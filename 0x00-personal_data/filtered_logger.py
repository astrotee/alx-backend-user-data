#!/usr/bin/env python3
"Regex-ing"
import os
import re
import logging
from typing import List
import mysql.connector


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


def get_db() -> mysql.connector.connection.MySQLConnection:
    "get a db connection"
    host = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    username = os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.environ.get('PERSONAL_DATA_DB_PASSWORD', '')
    database = os.environ.get('PERSONAL_DATA_DB_NAME', 'holberton')

    return mysql.connector.connection.MySQLConnection(host=host, user=username,
                                                      password=password,
                                                      database=database)


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


def main():
    logger = get_logger()
    cnx = get_db()
    cur = cnx.cursor(dictionary=True)
    cur.execute("SELECT * FROM users")
    columns = [col[0] for col in cur.column_names]
    for user in cur.fetchall():
        msg = ''.join(f"{col}={user[col]};" for col in columns)
        logger.info(msg)
    cur.close()
    cnx.close()


if __name__ == "__main__":
    main()
