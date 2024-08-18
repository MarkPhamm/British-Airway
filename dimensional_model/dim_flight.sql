IF OBJECT_ID('ba_review.dbo.dim_flight', 'U') IS NOT NULL
BEGIN
    DROP TABLE ba_review.dbo.dim_flight;
END
GO

SELECT 
    id AS customer_id, 
    month_year_fly, 
    aircraft_1, 
    aircraft_2, 
    origin, 
    destination, 
    transit
INTO ba_review.dbo.dim_flight
FROM ba_review.dbo.original;