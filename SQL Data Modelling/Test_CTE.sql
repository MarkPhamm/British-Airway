SELECT * FROM [ba_review].[dbo].[orginal];

WITH unique_country AS
(
    SELECT 
        distinct CASE WHEN country is null THEN 'Unknown' ELSE country END AS country 
    FROM ba_review.dbo.orginal
),
dim_customer as 
(
    SELECT 
        Distinct name as customer_name, 
        CASE WHEN country is null THEN 'Unknown' ELSE country END AS country 
    FROM ba_review.dbo.orginal
)
SELECT 
    row_number() over(order by country) as country_id,
    country 
FROM unique_country