SELECT
    loc.Location_Name,
    COUNT(DISTINCT vr.Rental_ID) AS num_rentals
FROM
    dm_locations as loc
    LEFT JOIN ft_vehicle_rentals as vr ON loc.Location_ID = vr.Location_ID
GROUP BY
    loc.Location_Name
;
