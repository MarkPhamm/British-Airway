-- Check if the table exists and drop it if it does
IF OBJECT_ID('ba_review.dbo.dim_review', 'U') IS NOT NULL
BEGIN
    DROP TABLE ba_review.dbo.dim_review;
END
GO

-- Create the dim_review table
CREATE TABLE ba_review.dbo.dim_review (
    review_id INT IDENTITY(1,1) PRIMARY KEY,
    customer_id INT NOT NULL,
    date_review DATE NOT NULL,
    review NVARCHAR(MAX)
);

-- Insert data into dim_review
INSERT INTO ba_review.dbo.dim_review (customer_id, date_review, review)
SELECT 
    id AS customer_id, 
    CAST(date_review AS DATE) AS date_review, 
    review
FROM ba_review.dbo.original;

-- Add indexes for better performance
CREATE NONCLUSTERED INDEX IX_dim_review_customer_id ON ba_review.dbo.dim_review (customer_id);
CREATE NONCLUSTERED INDEX IX_dim_review_date_review ON ba_review.dbo.dim_review (date_review);
