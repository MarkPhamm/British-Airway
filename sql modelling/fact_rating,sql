IF OBJECT_ID('ba_review.dbo.fact_rating', 'U') IS NOT NULL
BEGIN
    DROP TABLE ba_review.dbo.fact_rating;
END
GO

SELECT 
    original.id AS rating_id,
    original.verified,
    dim_customer.customer_id,
    original.date_review,
    original.month_year_fly AS date_flown,
    original.type AS traveller_type,
    original.seat_type,
    original.seat_comfort,
    original.cabit_serv,
    original.food,
    original.ground_service,
    original.wifi,
    original.money_value,
    original.recommended
INTO ba_review.dbo.fact_rating
FROM ba_review.dbo.original
JOIN ba_review.dbo.dim_customer ON original.name = dim_customer.customer_name;
