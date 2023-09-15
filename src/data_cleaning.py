import logging

from typing import List

import pandas as pd


def check_year_before_2023(date_str: str) -> bool:
    """
    Check if the year in a date string is before 2023.

    Args:
    - date_str (str): Date in the format 'dd/mm/yyyy'.

    Returns:
    - bool: True if the year is before 2023, False otherwise.
    """
    _, _, year = date_str.split("/")
    return int(year) < 2023


def replace_year_with_2023(date_str: str) -> str:
    """
    Replace the year in a date string with 2023 if it's before 2023.

    Args:
    - date_str (str): Date in the format 'dd/mm/yyyy'.

    Returns:
    - str: Updated date string.
    """
    if check_year_before_2023(date_str):
        day, month, _ = date_str.split("/")
        return f"{day}/{month}/2023"
    return date_str


def check_day_month_validity(date_str: str) -> bool:
    """
    Check the validity of day and month in a date string.

    Args:
    - date_str (str): Date in the format 'dd/mm/yyyy'.

    Returns:
    - bool: True if day and month are valid, False otherwise.
    """
    day, month, _ = date_str.split("/")
    return 1 <= int(day) <= 31 and 1 <= int(month) <= 12


def ensure_end_date_after_start_date(row: pd.Series) -> bool:
    """
    Check if the end date is after or equal to the start date in a DataFrame row.

    Args:
    - row (pd.Series): A row from a DataFrame with 'Start_Date' and 'End_Date' columns.

    Returns:
    - bool: True if 'End_Date' is after or equal to 'Start_Date', False otherwise.
    """
    start_date = pd.to_datetime(row["Start_Date"], format="%d/%m/%Y")
    end_date = pd.to_datetime(row["End_Date"], format="%d/%m/%Y")
    return end_date >= start_date


def clean_dates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the 'Start_Date' and 'End_Date' columns in a DataFrame.

    - Corrects years before 2023.
    - Removes rows with invalid start or end dates.
    - Converts dates to the ISO format 'YYYY-MM-DD'.

    Args:
    - df (pd.DataFrame): DataFrame with 'Start_Date' and 'End_Date' columns.

    Returns:
    - pd.DataFrame: A cleaned DataFrame with valid and properly formatted dates.
    """
    # Backup original data
    df_original = df.copy()

    df["Start_Date"] = df["Start_Date"].apply(replace_year_with_2023)
    df["End_Date"] = df["End_Date"].apply(replace_year_with_2023)

    corrected_dates_count = len(df[df_original["Start_Date"] != df["Start_Date"]])
    logging.info(f"Corrected year for {corrected_dates_count} rows.")

    # Filter rows with valid start and end dates
    valid_start_dates = df["Start_Date"].apply(check_day_month_validity)
    valid_end_dates = df["End_Date"].apply(check_day_month_validity)
    valid_rows = valid_start_dates & valid_end_dates

    logging.info(f"Removing {len(df) - sum(valid_rows)} rows due to invalid dates.")

    df_clean = df[valid_rows]

    # Convert dates to ISO format
    df_clean["Start_Date"] = pd.to_datetime(df_clean["Start_Date"], format="%d/%m/%Y")
    df_clean["End_Date"] = pd.to_datetime(df_clean["End_Date"], format="%d/%m/%Y")

    valid_dates = df_clean.apply(ensure_end_date_after_start_date, axis=1)

    df_clean = df_clean[valid_dates]

    return df_clean
