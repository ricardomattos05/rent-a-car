-- create_vehicles_table.sql

CREATE TABLE IF NOT EXISTS ft_vehicle_rentals (
    Rental_ID INTEGER PRIMARY KEY,
    Vehicle_ID INTEGER NOT NULL,
    Location_ID INTEGER NOT NULL,
    Start_Date DATE NOT NULL,
    End_Date DATE NOT NULL,
    FOREIGN KEY (Location_ID) REFERENCES dm_locations(Location_ID)
);
