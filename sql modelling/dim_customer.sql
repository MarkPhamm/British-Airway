IF OBJECT_ID('ba_review.dbo.dim_customer', 'U') IS NOT NULL
BEGIN
    DROP TABLE ba_review.dbo.dim_customer;
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
),

unique_customer AS
(
    SELECT 
        DISTINCT name AS customer_name, 
        CASE WHEN country IS NULL THEN 'Unknown' ELSE country END AS country 
    FROM ba_review.dbo.original
),
dim_customer_cte AS
(
    SELECT 
        ROW_NUMBER() OVER(ORDER BY uc.customer_name) AS customer_id,
        customer_name,
        dc_cte.country_id
    FROM unique_customer uc
    JOIN dim_country_cte as dc_cte
    ON uc.country = dc_cte.country
) 

SELECT * 
INTO ba_review.dbo.dim_customer
FROM dim_customer_cte
ORDER  BY customer_id, country_id
