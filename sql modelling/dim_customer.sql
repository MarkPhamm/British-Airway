with unique_customer AS
(
    SELECT 
        Distinct name as customer_name, 
        CASE WHEN country is null THEN 'Unknown' ELSE country END AS country 
    FROM ba_review.dbo.original
),
dim_customer_cte AS
(
SELECT 
    row_number() over(order by unique_customer.country) as customer_id,
    customer_name,
    country_id
FROM unique_customer
JOIN ba_review.dbo.dim_country 
ON dim_country.country = unique_customer.country
) 
SELECT * 
FROM dim_customer_cte
