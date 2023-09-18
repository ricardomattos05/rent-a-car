WITH rental_duration as (
    SELECT
        Location_ID,
        Vehicle_ID,
        SUM(
            (julianday(End_Date) - julianday(Start_Date) + 1)
        ) as rental_days
    FROM
        ft_vehicle_rentals
    GROUP BY
        Location_ID,
        Vehicle_ID
),
location_summary as (
    SELECT
        loc.Location_Name,
        sum(rental_days) as total_rental_days,
        COUNT(DISTINCT rd.Vehicle_ID) AS fleet_size,
        (
            SELECT
                julianday(MAX(End_Date)) - julianday(MIN(Start_Date)) + 1
            FROM
                ft_vehicle_rentals
        ) as available_days
    FROM
        dm_locations as loc
        LEFT JOIN rental_duration as rd ON loc.Location_ID = rd.Location_ID
    GROUP BY
        loc.Location_Name
)
SELECT
    Location_Name,
    total_rental_days /(fleet_size * available_days) as utilization_rate
FROM
    location_summary;
