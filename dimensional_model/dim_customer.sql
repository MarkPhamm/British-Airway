-- Check if the table exists and drop it if it does
IF OBJECT_ID('ba_review.dbo.dim_customer', 'U') IS NOT NULL
BEGIN
    DROP TABLE ba_review.dbo.dim_customer;
END
GO

-- Create the dim_customer table
CREATE TABLE ba_review.dbo.dim_customer (
    customer_id INT IDENTITY(1,1) PRIMARY KEY,
    customer_name NVARCHAR(255) NOT NULL,
    country_id INT NOT NULL
);

-- Insert data into dim_customer
INSERT INTO ba_review.dbo.dim_customer (customer_name, country_id)
SELECT 
    uc.customer_name,
    dc.country_id
FROM 
    (SELECT DISTINCT 
        COALESCE(name, 'Unknown') AS customer_name, 
        COALESCE(country, 'Unknown') AS country
    FROM ba_review.dbo.original) AS uc
JOIN ba_review.dbo.dim_country AS dc ON uc.country = dc.country
ORDER BY uc.customer_name;

-- Add an index on the country_id column for better performance
CREATE NONCLUSTERED INDEX IX_dim_customer_country_id ON ba_review.dbo.dim_customer (country_id);
