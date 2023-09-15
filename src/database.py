import sqlite3

from typing import List
from typing import Tuple


class DatabaseError(Exception):
    """Custom exception class for database-related errors."""

    pass


def create_connection(database_name: str) -> sqlite3.Connection:
    """
    Establish a connection to an SQLite database.

    Args:
    - database_name (str): The name (or path) of the SQLite database.

    Returns:
    - sqlite3.Connection: The database connection object.

    Raises:
    - DatabaseError: If a connection cannot be established.
    """
    try:
        conn = sqlite3.connect(database_name)
        return conn
    except sqlite3.Error as e:
        raise DatabaseError(f"Connection error: {e}")


def execute_query(conn: sqlite3.Connection, query: str) -> None:
    """
    Execute a single SQL query using an active database connection.

    Args:
    - conn (sqlite3.Connection): The database connection object.
    - query (str): The SQL query to be executed.

    Raises:
    - DatabaseError: If the query execution fails.
    """
    try:
        with conn:
            conn.execute(query)
    except sqlite3.Error as e:
        raise DatabaseError(f"Failed to execute query. Error: {e}")


def execute_many_query(conn: sqlite3.Connection, query: str, data: List[Tuple]) -> None:
    """
    Execute a single SQL query multiple times with different data.

    Args:
    - conn (sqlite3.Connection): The database connection object.
    - query (str): The SQL query template to be executed.
    - data (List[Tuple]): A list of tuples, each representing a row of data to be inserted.

    Raises:
    - DatabaseError: If the query execution fails.
    """
    try:
        with conn:
            conn.executemany(query, data)
    except sqlite3.Error as e:
        raise DatabaseError(f"Failed to execute many query. Error: {e}")


def fetch_query(conn: sqlite3.Connection, query: str) -> List[Tuple]:
    """
    Execute an SQL query and fetch the results.

    Args:
    - conn (sqlite3.Connection): The database connection object.
    - query (str): The SQL query to be executed.

    Returns:
    - List[Tuple]: A list of tuples, each representing a row of fetched data.

    Raises:
    - DatabaseError: If the query execution or fetching fails.
    """
    try:
        with conn:
            cur = conn.cursor()
            cur.execute(query)
            return cur.fetchall()
    except sqlite3.Error as e:
        raise DatabaseError(f"Failed to fetch query. Error: {e}")


def create_index(conn: sqlite3.Connection, table_name: str, column_name: str) -> None:
    """
    Create an index on a specific column in a table to improve query performance.

    Args:
    - conn (sqlite3.Connection): The database connection object.
    - table_name (str): The name of the table where the index should be created.
    - column_name (str): The name of the column on which the index should be created.

    Note:
    - The index will only be created if it does not already exist.

    Raises:
    - DatabaseError: If there's an error during the index creation process.
    """
    query = f"CREATE INDEX IF NOT EXISTS idx_{table_name}_{column_name} ON {table_name}({column_name})"
    execute_query(conn, query)


def load_sql_from_file(file_path: str) -> str:
    """
    Load SQL commands from a specified file.

    Args:
    - file_path (str): The path to the SQL file.

    Returns:
    - str: The SQL commands loaded from the file.

    Raises:
    - IOError: If there's an error reading the file.
    """
    with open(file_path, "r") as f:
        return f.read()


def setup_database(conn: sqlite3.Connection, sql_files: List[str]) -> None:
    """
    Initialize the database using SQL scripts from provided files.

    Args:
    - conn (sqlite3.Connection): The database connection object.
    - sql_files (List[str]): A list of paths to the SQL files.

    Raises:
    - DatabaseError: If any error occurs during the setup process.
    """
    for sql_file in sql_files:
        query = load_sql_from_file(sql_file)
        execute_query(conn, query)
