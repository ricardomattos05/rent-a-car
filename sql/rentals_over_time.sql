SELECT
    Start_Date as date,
    COUNT(DISTINCT Rental_ID) AS num_rentals
FROM
    ft_vehicle_rentals
GROUP BY
    Start_Date;
