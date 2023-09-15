-- create_vehicles_table.sql

CREATE TABLE IF NOT EXISTS Vehicle_Rentals (
    Rental_ID INTEGER PRIMARY KEY,
    Vehicle_ID INTEGER NOT NULL,
    Location_ID INTEGER NOT NULL,
    Start_Date TEXT NOT NULL,
    End_Date TEXT NOT NULL,
    FOREIGN KEY (Location_ID) REFERENCES Locations(Location_ID)
);
