"""Functions for setting up and interacting with the SQLite database."""

import sqlite3


def setup_db(database_path: str):
    """Sets up the SQLite database and creates the tables if neccessary."""

    db = sqlite3.connect(database_path)

    columns = [
        "message_id TEXT NOT NULL PRIMARY KEY",
        "author_id TEXT NOT NULL",
        "curated_message_id TEXT NOT NULL",
        "curation_date_iso TEXT NOT NULL",
    ]

    with db:
        db.cursor().execute(
            f"CREATE TABLE IF NOT EXISTS curations ({','.join(columns)})"
        )

    return db


def get_curation_from_db(conn: sqlite3.Connection, message_id: int):
    """Returns a curation from the curations table."""

    with conn:
        return (
            conn.cursor()
            .execute(
                "SELECT * FROM curations WHERE message_id = ?",
                (message_id,),
            )
            .fetchone()
        )


def insert_curation_to_db(
    conn: sqlite3.Connection,
    message_id: int,
    author_id: int,
    curated_message_id: int,
    curation_date_iso: str,
):
    """Inserts a curation into the curations table."""

    with conn:
        conn.cursor().execute(
            "INSERT INTO curations VALUES (?, ?, ?, ?)",
            (
                message_id,
                author_id,
                curated_message_id,
                curation_date_iso,
            ),
        )
