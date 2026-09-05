import sqlite3
from datetime import datetime


DATABASE_NAME = "resume_analyzer.db"


def get_connection():

    connection = sqlite3.connect(DATABASE_NAME)

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            resume_filename TEXT NOT NULL,

            match_percentage INTEGER NOT NULL,

            matching_skills TEXT,

            missing_skills TEXT,

            created_at TEXT NOT NULL
        )
    """)

    connection.commit()

    connection.close()


def save_analysis(
    resume_filename,
    match_percentage,
    matching_skills,
    missing_skills
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO analyses
        (
            resume_filename,
            match_percentage,
            matching_skills,
            missing_skills,
            created_at
        )

        VALUES (?, ?, ?, ?, ?)
    """, (

        resume_filename,
        match_percentage,
        ", ".join(matching_skills),
        ", ".join(missing_skills),
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    ))

    connection.commit()

    connection.close()


def get_all_analyses():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM analyses
        ORDER BY id DESC
    """)

    analyses = cursor.fetchall()

    connection.close()

    return analyses