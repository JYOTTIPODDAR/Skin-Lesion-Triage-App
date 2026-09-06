import sqlite3
import os
from datetime import datetime


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DB_PATH = os.path.join(
    BASE_DIR,
    "skintriage.db"
)


def get_connection():

    connection = sqlite3.connect(DB_PATH)

    connection.row_factory = sqlite3.Row

    return connection


def create_history_table():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analysis_history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            filename TEXT,

            prediction TEXT NOT NULL,

            confidence REAL NOT NULL,

            risk_level TEXT NOT NULL,

            result_title TEXT,

            recommendation TEXT,

            created_at TEXT NOT NULL

        )
    """)

    connection.commit()

    connection.close()


def save_analysis(
    filename,
    prediction,
    confidence,
    risk_level,
    result_title,
    recommendation
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO analysis_history (
            filename,
            prediction,
            confidence,
            risk_level,
            result_title,
            recommendation,
            created_at
        )

        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (

        filename,
        prediction,
        confidence,
        risk_level,
        result_title,
        recommendation,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ))

    connection.commit()

    connection.close()