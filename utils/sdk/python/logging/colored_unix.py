"""Provides a custom logging formatter that adds colors to log messages based on their severity level."""

import logging
import sys
import typing


class CustomFormatter(logging.Formatter):
    """Custom formatter to add colors to log messages based on their severity level."""

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)-8s | %(message)s (%(filename)s:%(lineno)d)"

    FORMATS: typing.ClassVar[dict] = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record: logging.LogRecord) -> str:
        """Format the specified record as text.

        Args:
            record (logging.LogRecord): The log record to be formatted.

        Returns:
            str: The formatted log record as a string.

        """
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


# create logger with 'spam_application'
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

ch.setFormatter(CustomFormatter())

logger.addHandler(ch)

logger.addHandler(logging.FileHandler(filename="foo.log"))
logger.addHandler(logging.StreamHandler(stream=sys.stdout))


logger.debug("debug message")
logger.info("info message")
logger.warning("warning message")
logger.error("error message")
logger.critical("critical message")
