-- Check if the table exists and drop it if it does
IF OBJECT_ID('ba_review.dbo.dim_flight', 'U') IS NOT NULL
BEGIN
    DROP TABLE ba_review.dbo.dim_flight;
END
GO

-- Create the dim_flight table
CREATE TABLE ba_review.dbo.dim_flight (
    flight_id INT IDENTITY(1,1) PRIMARY KEY,
    customer_id INT NOT NULL,
    month_year_fly DATE NOT NULL,
    aircraft_1 NVARCHAR(255),
    aircraft_2 NVARCHAR(255),
    origin NVARCHAR(255),
    destination NVARCHAR(255),
    transit NVARCHAR(255)
);

-- Insert data into dim_flight
INSERT INTO ba_review.dbo.dim_flight (customer_id, month_year_fly, aircraft_1, aircraft_2, origin, destination, transit)
SELECT 
    id AS customer_id, 
    CAST(month_year_fly AS DATE) AS month_year_fly,
    NULLIF(aircraft_1, '') AS aircraft_1,
    NULLIF(aircraft_2, '') AS aircraft_2,
    NULLIF(origin, '') AS origin,
    NULLIF(destination, '') AS destination,
    NULLIF(transit, '') AS transit
FROM ba_review.dbo.original;

-- Add indexes for better performance
CREATE NONCLUSTERED INDEX IX_dim_flight_customer_id ON ba_review.dbo.dim_flight (customer_id);
CREATE NONCLUSTERED INDEX IX_dim_flight_month_year_fly ON ba_review.dbo.dim_flight (month_year_fly);