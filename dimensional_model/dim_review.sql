IF OBJECT_ID('ba_review.dbo.dim_review', 'U') IS NOT NULL
BEGIN
    DROP TABLE ba_review.dbo.dim_review;
END
GO

SELECT 
    id AS customer_id, 
    date_review, 
    review
INTO ba_review.dbo.dim_review
FROM ba_review.dbo.original;
