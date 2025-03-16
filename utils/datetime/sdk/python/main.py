from __future__ import annotations

import calendar
import datetime
from string import Template
from typing import Optional, Union

import numpy as np
import pandas as pd
import pytz


def str2datetime(
        value: Union[str, datetime.datetime, pd.Series, list],
        errors: str = "raise",
        format_list: Optional[list[str]] = None,
) -> Union[datetime.datetime, pd.Series]:
    """Convert string to datetime object.

    :param value: string, datetime.datetime, pd.Series, list
    :param errors: how to handle errors
    :param format_list: list of datetime formats to try
    :return: datetime.datetime value corresponding to given string
    """
    if format_list is None:
        format_list = ["%Y-%m-%d %H:%M:%S",
                       "%d/%m/%Y %H:%M:%S",
                       "%d/%m/%y %H:%M:%S",
                       "%d.%m.%Y %H:%M:%S",
                       "%d.%m.%y %H:%M:%S",
                       "%d.%m.%Y %H.%M",
                       "%d.%m.%y %H.%M",
                       "%d.%m.%Y %H.%M.%S",
                       "%d.%m.%y %H.%M.%S"]

    # convert str, list to pandas Series
    series_values = value
    try:
        if isinstance(series_values, pd.Series) and series_values.empty:
            return None
    except AttributeError:
        if isinstance(series_values, list):
            series_values = pd.Series(series_values)
        series_values = pd.Series([series_values])

    # input correction: replace double whitespace character to single space
    try:
        for index, series_val in series_values.items():
            series_values[index] = series_val.str.trim().replace(pat=r"\s{2,}", repl=" ", regex=True)
    except AttributeError:
        pass

    series_response = pd.Series(np.zeros(len(series_values)) * np.nan)

    for form in format_list:
        try:  # vectorized process
            mask = series_response.isnull()
            if mask.any():
                series_response.loc[mask] = pd.to_datetime(
                    arg=series_values[mask], errors="coerce", utc=None, format=form)
        except (AttributeError, ValueError):  # if ValueError: cannot convert float NaN to integer
            for index, value in series_response.items():
                if pd.isna(value):
                    series_response.loc[index] = pd.to_datetime(
                        arg=series_values[index], errors="coerce", utc=None, format=form)


    # Try to convert other recognized formats
    mask = series_response.isna()
    if mask.any():
        try:  # vectorized process
            for index, value in series_response.items():
                if pd.isna(value):
                    series_response.loc[index] = pd.to_datetime(arg=series_values[index], errors="coerce")
        except (AttributeError, ValueError):  # if ValueError: cannot convert float NaN to integer
            series_response.loc[mask] = pd.to_datetime(arg=series_values[mask], errors="coerce")

    # Convert format #####.##### (eg. 42139.23213)
    mask = series_response.isna()
    if mask.any():
        try:  # vectorized process
            for index, value in series_response.items():
                if pd.isna(value):
                    series_response.loc[index] = xlserialdate_to_datetime(series_values.loc[index], errors=errors)
        except (AttributeError, ValueError):  # if ValueError: cannot convert float NaN to integer
            series_response.loc[mask] = series_values.loc[mask].apply(lambda x: xlserialdate_to_datetime(x, errors=errors))

    # Handle error if still missing
    mask = series_response.isna()
    if mask.any():
        errmsg = f'Failed to recognize datetime format, please use one of these formats: "{format_list}"'
        if errors == "raise":
            raise ValueError(errmsg)

    return series_response

def xlserialdate_to_datetime(
        xlserialdate: float,
        errors: str = "ignore",
) -> Union[datetime.datetime, float]:
    """Convert a Microsoft Excel serial date to datetime object.

    :param xlserialdate: Microsoft Excel serial date
    :param errors: how to handle errors
    :return: datetime.datetime value corresponding to given serial date
    """
    minutes_in_hour = 60
    try:
        xlserialdate = float(xlserialdate)
        excel_anchor = datetime.datetime(1900, 1, 1, tzinfo=pytz.utc)
        offset = 2 if xlserialdate >= minutes_in_hour else 1
        converted_date = excel_anchor + datetime.timedelta(days=(xlserialdate - offset))
        hour, r = divmod((xlserialdate % 1), 1)
        minute, r = divmod(r * 60, 1)
        second = r * 60
        return converted_date.replace(hour=int(hour), minute=int(minute), second=int(second)).round("1min")
    except Exception:
        if errors == "ignore":
            return xlserialdate
        if errors == "coerce":
            return pd.NaT
        raise


def str2time(df_values: pd.DataFrame) -> pd.Series:
    """Convert string to time object.

    :param df_values: pandas DataFrame
    :return: time object corresponding to given string
    """
    df_values = df_values.to_frame(name="values")
    df_values_formatted = pd.to_datetime(arg=df_values["values"],
                                         errors="coerce", utc=None,
                                         format="%H:%M")
    mask = df_values_formatted.isna()
    df_values_formatted.loc[mask] = pd.to_datetime(
        arg=df_values[mask]["values"],
        errors="coerce", utc=None,
        format="%H:%M:%S",
    )

    mask = df_values_formatted.isna()
    df_values_formatted.loc[mask] = pd.to_datetime(
        arg=df_values[mask]["values"],
        errors="coerce",
    )

    return df_values_formatted.dt.time


def is_datetime_between(
        start_datetime_incl: datetime.datetime,
        end_datetime_excl: datetime.datetime,
        check_datetime: Optional[datetime.datetime] = None,
        tz: Optional[str] = None,
) -> bool:
    """Check if a datetime is between two other datetimes.

    :param start_datetime_incl: start datetime (inclusive)
    :param end_datetime_excl: end datetime (exclusive)
    :param check_datetime: datetime to check
    :param tz: timezone
    :return: True if check datetime is between start and end datetimes
    """
    # If check time is not given, default to current UTC time
    check_datetime = check_datetime or datetime.datetime.now(tz=pytz.timezone(tz or "Etc/UTC"))
    if start_datetime_incl < end_datetime_excl:
        return start_datetime_incl <= check_datetime <= end_datetime_excl
    raise ValueError("End datetime (excl) is not greater than start datetime (incl)")


def is_time_between(
        start_time_incl: datetime.time,
        end_time_excl: datetime.time,
        check_time: Optional[datetime.time] = None,
        tz: Optional[str] = None,
) -> bool:
    """Check if a time is between two other.

    :param start_time_incl: start time (inclusive)
    :param end_time_excl: end time (exclusive)
    :param check_time: time to check
    :param tz: timezone
    :return: True if check time is between start and end times
    """
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.datetime.now(tz=pytz.timezone(tz or "Etc/UTC")).time()
    if start_time_incl < end_time_excl:
        return start_time_incl <= check_time <= end_time_excl
    # crosses midnight
    return check_time >= start_time_incl or check_time <= end_time_excl


def strfdelta(tdelta: datetime.timedelta, fmt: str) -> str:
    """Format timedelta object.

    :param tdelta: datetime.timedelta object
    :param fmt: output format specification eg. %D days %H:%M:%S
    :return: formatted timedelta string
    """

    class DeltaTemplate(Template):
        delimiter = "%"

    d = {"D": tdelta.days}
    hours, rem = divmod(tdelta.seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    d["H"] = hours
    d["M"] = minutes
    d["S"] = seconds
    t = DeltaTemplate(fmt)
    return t.substitute(**d)


def add_one_month(orig_date: datetime.datetime) -> datetime.datetime:
    """Add one month to a date.

    :param orig_date: original date
    :return: date with one month added
    """
    months_in_year = 12
    # advance year and month by one month
    new_year = orig_date.year
    new_month = orig_date.month + 1
    # note: in datetime.date, months go from 1 to 12
    if new_month > months_in_year:
        new_year += 1
        new_month -= months_in_year

    last_day_of_month = calendar.monthrange(new_year, new_month)[1]
    new_day = min(orig_date.day, last_day_of_month)

    return orig_date.replace(year=new_year, month=new_month, day=new_day)
