IF OBJECT_ID('ba_review.dbo.dim_country', 'U') IS NOT NULL
BEGIN
    DROP TABLE ba_review.dbo.dim_country;
END
GO

WITH unique_country AS
(
    SELECT 
        DISTINCT CASE WHEN country IS NULL THEN 'Unknown' ELSE country END AS country 
    FROM ba_review.dbo.original
),
dim_country_cte AS
(
    SELECT 
        ROW_NUMBER() OVER(ORDER BY country) AS country_id,
        country 
    FROM unique_country
)

SELECT * INTO ba_review.dbo.dim_country
FROM dim_country_cte;
