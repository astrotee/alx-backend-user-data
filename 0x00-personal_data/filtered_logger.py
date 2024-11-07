#!/usr/bin/env python3
"Regex-ing"
import re
import logging
from typing import List


PII_FIELDS = ["name", "email", "phone", "ssn", "password"]


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    "filte sensitive fields"
    return re.sub(f"({'|'.join(fields)})=.*?{separator}",
                  rf"\1={redaction}{separator}", message)


def get_logger() -> logging.Logger:
    "return a logger instance"
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    return logger


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        "filter fields before formatting"
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)
