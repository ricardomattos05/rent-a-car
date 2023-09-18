SELECT
    loc.Location_Name,
    ROUND(
        (
            SUM(
                (
                    julianday(rd.End_Date) - julianday(rd.Start_Date) + 1
                )
            ) / COUNT(DISTINCT rd.Rental_ID)
        ),
        2
    ) as avg_rental_days
FROM
    ft_vehicle_rentals as rd
    LEFT JOIN dm_locations as loc ON loc.Location_ID = rd.Location_ID
GROUP BY
    loc.Location_Name;
