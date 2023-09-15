-- create_locations_table.sql

CREATE TABLE IF NOT EXISTS Locations (
    Location_ID INTEGER PRIMARY KEY,
    Location_Name TEXT NOT NULL,
    City TEXT NOT NULL,
    Country TEXT NOT NULL
);
