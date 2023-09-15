import configparser
import logging

from data_ingestion import insert_data_from_csv_to_db
from database import DatabaseError
from database import create_connection
from database import create_index
from database import setup_database


logging.basicConfig(filename="logs/application.log", level=logging.INFO)


def main():
    """
    The main function to initiate the database setup and data ingestion processes.

    - Loads the configurations from `config.ini`.
    - Sets up the SQLite database based on SQL files specified in the configurations.
    - Ingests data from specific CSV files into the corresponding tables in the database.
    - Logs the progress and any potential errors encountered during the process.
    """
    config = configparser.ConfigParser()
    config.read("config.ini")

    sql_files = config.get("PATHS", "SQL_FILES").split(", ")
    database_name = f"data/{config['DATABASE']['NAME']}"

    conn = None

    try:
        conn = create_connection(database_name)

        logging.info("Starting database setup.")
        setup_database(conn, sql_files)
        logging.info("Database setup completed.")

        insert_data_from_csv_to_db(conn, "data/Vehicle_Rentals.csv", "ft_vehicle_Rentals")
        insert_data_from_csv_to_db(conn, "data/Locations.csv", "dm_locations")

        create_index(conn, "ft_vehicle_Rentals", "Location_ID")
        create_index(conn, "ft_vehicle_Rentals", "Rental_ID")
        create_index(conn, "dm_locations", "Location_ID")

        logging.info("Initialization and data ingestion were successful!")

    except DatabaseError as e:
        logging.error(e)

    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    main()
