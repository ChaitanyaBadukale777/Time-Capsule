# backend/db_config.py

import mysql.connector

# 🔧 CHANGE THESE ACCORDING TO YOUR MYSQL SETUP
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "root123"
DB_NAME = "digital_time_capsule"


def get_connection():
    """
    Returns a new MySQL connection.
    """
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
