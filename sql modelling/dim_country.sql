-- CREATE TABLE ba_review.dbo.dim_country (
--     country_id INT primary key,
--     country VARCHAR(255) -- Adjust the length as needed
-- );

-- DROP TABLE IF EXISTS ba_review.dbo.dim_country

WITH unique_country AS
(
    SELECT 
        distinct CASE WHEN country is null THEN 'Unknown' ELSE country END AS country 
    FROM ba_review.dbo.original
),
dim_country_cte AS
(
    SELECT 
        row_number() over(order by country) as country_id,
        country 
    FROM unique_country
)
SELECT * 
FROM dim_country_cte

