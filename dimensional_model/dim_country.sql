-- Check if the table exists and drop it if it does
IF OBJECT_ID('ba_review.dbo.dim_country', 'U') IS NOT NULL
BEGIN
    DROP TABLE ba_review.dbo.dim_country;
END
GO

-- Create the dim_country table
CREATE TABLE ba_review.dbo.dim_country (
    country_id INT IDENTITY(1,1) PRIMARY KEY,
    country NVARCHAR(255) NOT NULL
);

-- Insert data into dim_country
INSERT INTO ba_review.dbo.dim_country (country)
SELECT DISTINCT 
    COALESCE(country, 'Unknown') AS country
FROM ba_review.dbo.original
ORDER BY country;

-- Add an index on the country column for better performance
CREATE NONCLUSTERED INDEX IX_dim_country_country ON ba_review.dbo.dim_country (country);
