"""Parameterized SQL queries using SQLite."""
import sqlite3


def find_user(connection: sqlite3.Connection, username: str):
    """Find a user without concatenating input into SQL."""
    return connection.execute(
        "SELECT id, username FROM users WHERE username = ?",
        (username,),
    ).fetchone()


def main() -> None:
    connection = sqlite3.connect(":memory:")
    try:
        connection.execute(
            "CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT NOT NULL)"
        )
        connection.executemany(
            "INSERT INTO users (username) VALUES (?)",
            [("alice",), ("bob",)],
        )
        supplied_username = input("Username to search: ")
        print(find_user(connection, supplied_username))
    finally:
        connection.close()


if __name__ == "__main__":
    main()
