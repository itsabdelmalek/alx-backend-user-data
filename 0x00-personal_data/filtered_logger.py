#!/usr/bin/env python3
"""
This module provides functions for logging, data obfuscation,
and database connection.
"""


import logging
import os
import re
from typing import List
import mysql.connector

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Obfuscate specified fields in a log message"""
    for i in fields:
        message = re.sub(rf"{i}=(.*?)\{separator}",
                         f'{i}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """RedactingFormatter class."""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize RedactingFormatter."""
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """Format log record with redaction."""
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def get_logger() -> logging.Logger:
    """Create and configure a logging.Logger object."""

    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    return logger


def get_db() -> connection.MySQLConnection:
    """returns a connector to the database"""
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    return connection.MySQLConnection(
            host=host,
            username=username,
            password=password,
            database=db_name
            )


def main() -> None:
    """
    Obtain a database connection, retrieve all rows in the users table,
    and display each row in a filtered format
    """
    db_connector = get_db()
    cursor = db_connector.cursor()
    cursor.execute("SELECT * FROM users;")
    for row in cursor:
        message = f"name={row[0]}; email={row[1]}; phone={row[2]}; " +\
            f"ssn={row[3]}; password={row[4]};ip={row[5]}; " +\
            f"last_login={row[6]}; user_agent={row[7]};"
        print(message)
    cursor.close()
    db_connector.close()


if __name__ == '__main__':
    main()
