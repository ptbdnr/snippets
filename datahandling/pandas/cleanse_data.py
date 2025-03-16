from __future__ import annotations

import logging
import sys
from typing import Optional, Union

import numpy as np
import pandas as pd
import scipy.stats
import sklearn.ensemble


class DataCleanser:
    df: pd.DataFrame
    logger: logging.Logger

    def __init__(
            self,
            df: pd.DataFrame,
            *,
            inplace: Optional[bool] = False,
            logger: Optional[logging.Logger] = None,
    ) -> None:
        """Initialize the DataCleanser object.

        :param df: object of type pandas.DataFrame
        :param inplace: boolean flag to update the object in place, default is False
        :param logger: object of type logging.Logger
        """
        if inplace:
            self.df = df.copy(deep=True)
        else:
            self.df = df

        if logger is None:
            self.logger = logging.getLogger(__name__)
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                "%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)-s - %(funcName)s()] %(message)s")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.DEBUG)

    def build(self) -> pd.DataFrame:
        """Return cleansed observations.

        :return: cleansed object of type pandas.DataFrame
        """
        return self.df

    def drop_duplicates(self) -> "DataCleanser":
        """Identify duplicate records.

        Keep only first instance of each duplicate, drop any further instance.
        :return: self, object of CleaseData class
        """
        self.logger.info("Identify and remove duplicates")

        self.df.drop_duplicates(keep="first", inplace=True, ignore_index=False)

        self.logger.debug(f"Number of records to keep: {len(self.df)}")

        return self

    def drop_empty_values(
            self,
            target_features: list[str],
    ) -> "DataCleanser":
        """Drop records with missing data.

        :param target_features:
        :return: self, object of CleaseData class
        """
        self.logger.info("Identify and remove anomaly missing data")

        self.df.dropna(axis=0, how="any", thresh=None, subset=target_features, inplace=True)

        self.logger.debug(f"Number of records to keep: {len(self.df)}")

        return self

    def drop_outliers_using_iqr(
            self,
            target_features: list[str],
            k: float = 3,
            q_min: float = 0.25,
            q_max: float = 0.75,
    ) -> "DataCleanser":
        """Drop outliers.

        Use the Interquartile Range (IQR), aka midspread, which is a measure of statistical dispersion,
        to classify observations into inlier or outlier classes - on each target feature and drop outliers.
        :param target_features: list of column names that contain the target features
        :param k: float number to tune the range width,  k=3 as per Tukey, 1977
        :param q_min: float number to define the lower threshold of the range
        :param q_max: float number to define the upper threshold of the range
        :return: self, object of CleaseData class
        """
        self.logger.info("Identify and remove anomaly using IQR")

        for c in target_features:
            c_q_min = self.df[c].quantile(q=q_min, interpolation="midpoint")
            c_q_max = self.df[c].quantile(q=q_max, interpolation="midpoint")

            c_iqr = scipy.stats.iqr(self.df[c], interpolation="midpoint")  # c_q_max - c_q_min

            c_low_limit = c_q_min - k * c_iqr
            c_high_limit = c_q_max + k * c_iqr

            condition = (c_low_limit <= self.df[c]) & (self.df[c] <= c_high_limit)
            self.df = self.df[condition].copy()

            self.logger.debug("Number of records to drop: %d", np.count_nonzero(~condition))
            self.logger.debug("Number of records to keep: %d", len(self.df))

        return self

    def drop_outliers_using_z_score(
            self,
            target_features: list[str],
            threshold: float = 3,
    ) -> "DataCleanser":
        """Drop outliers.

        Use the Z-score - which is the signed number of standard deviations by which the value of an observation
        is above the mean value, to classify observations into inlier or outlier classes - on each target feature
        and drop outliers. This modification also works on small datasets with fewer than 12 records.
        :param target_features: list of column names that contain the target features
        :param threshold: float number to define range width, t=3 as per Dienes, 2010.
        :return: self, object of CleaseData class
        """
        self.logger.info("Identify and remove anomaly using z-score")

        for c in target_features:
            median_y = np.median(self.df[c])
            median_absolute_deviation_y = np.median([np.abs(y - median_y) for y in self.df[c]])
            modified_z_scores = [0.6745 * (y - median_y) / median_absolute_deviation_y
                                 for y in self.df[c]]
            condition = (np.abs(modified_z_scores) <= threshold)
            self.df = self.df[condition].copy()

            self.logger.debug("Number of records to drop: %d", np.count_nonzero(~condition))
            self.logger.debug("Number of records to keep: %d", len(self.df))

        return self

    def drop_outliers_using_isolation_forest(
            self,
            target_features: list[str],
            contamination: Union[float, str] = "auto",
     ) -> "DataCleanser":
        """Drop outliers.

        Use the Isolation Forest algorithm - which is an unsupervised machine learning estimator
        to classify observations into inlier or outlier classes - on each target feature and drop outliers.
        See: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html
        :param target_features: list of column names that contain the target features
        :param contamination: the amount of contamination of the data set, i.e. the proportion of outliers
            in the data set. Used when fitting to define the threshold on the scores of the samples.
            'auto' uses the threshold from Liu et al., 2008
        :return: self, object of CleaseData class
        """
        self.logger.info("Identify and remove anomaly using Isolation Forest ML algorithm")

        if isinstance(contamination, float) and (contamination < 0 or contamination > 0.5):
            self.logger.error("contamination should be in the range [0, 0.5], but received %s", contamination)

        # Create estimator
        isolation_forest = sklearn.ensemble.IsolationForest(
            random_state=0,
            contamination=contamination,
            n_jobs=1)
        # Fit estimator
        isolation_forest.fit(self.df[target_features])
        # Predict if a particular sample is an outlier or not: For each observation,
        # tells whether or not (+1 or -1) it should be considered as an inlier according to the fitted estimator.
        #  -1 for outliers and 1 for inliers.
        classification = isolation_forest.predict(self.df[target_features])
        condition = (classification == +1)
        self.df = self.df[condition].copy()

        self.logger.debug("Number of records to drop: %d", np.count_nonzero(~condition))
        self.logger.debug("Number of records to keep: %d", len(self.df))

        return self

