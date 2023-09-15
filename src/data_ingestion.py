import csv
import sqlite3

import pandas as pd

from data_cleaning import clean_dates
from database import DatabaseError
from database import execute_many_query


def detect_delimiter(file_name: str) -> str:
    """
    Determine the delimiter used in a CSV file based on its file name.

    Args:
    - file_name (str): The name (or path) of the CSV file.

    Returns:
    - str: The delimiter used in the CSV, either a comma (",") or semicolon (";").
    """
    return ";" if "Locations" in file_name else ","


def insert_data_from_csv_to_db(conn: sqlite3.Connection, file_path: str, table_name: str) -> None:
    """
    Ingest data from a CSV file into a specific table in the SQLite database.

    Args:
    - conn (sqlite3.Connection): The database connection object.
    - file_path (str): The path to the CSV file to be ingested.
    - table_name (str): The name of the table where the CSV data should be inserted.

    Raises:
    - DatabaseError: If any error occurs during the data ingestion process.
    """
    delimiter = detect_delimiter(file_path)

    try:
        df = pd.read_csv(file_path, delimiter=delimiter)

        # Clean the data if it's from the Vehicle_Rentals.csv
        if table_name == "ft_vehicle_Rentals":
            df = clean_dates(df)

        # Convert the cleaned DataFrame back to CSV format to use the original insertion logic
        data_to_insert = df.to_csv(index=False, header=True, sep=delimiter).split("\n")

        dr = csv.DictReader(data_to_insert, delimiter=delimiter)
        columns = dr.fieldnames
        query = f"INSERT OR IGNORE INTO {table_name} ({','.join(columns)}) VALUES ({','.join(['?' for _ in columns])})"

        for row in dr:
            values = tuple(row[col] for col in columns)
            execute_many_query(conn, query, [values])

    except Exception as e:
        raise DatabaseError(f"Failed to insert data from {file_path}. Error: {e}")
