-- Check if the table exists and drop it if it does
IF OBJECT_ID('ba_review.dbo.fact_rating', 'U') IS NOT NULL
BEGIN
    DROP TABLE ba_review.dbo.fact_rating;
END
GO

-- Create the fact_rating table
CREATE TABLE ba_review.dbo.fact_rating (
    rating_id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    review_id INT NOT NULL,
    flight_id INT NOT NULL,
    time_id INT NOT NULL,
    verified BIT NOT NULL,
    traveller_type NVARCHAR(50),
    seat_type NVARCHAR(50),
    seat_comfort TINYINT,
    cabin_service TINYINT,
    food TINYINT,
    ground_service TINYINT,
    wifi TINYINT,
    money_value TINYINT,
    recommended BIT
);

-- Insert data into fact_rating
INSERT INTO ba_review.dbo.fact_rating (
    rating_id, customer_id, review_id, flight_id, time_id, verified, 
    traveller_type, seat_type, seat_comfort, cabin_service, food, 
    ground_service, wifi, money_value, recommended
)
SELECT 
    o.id AS rating_id,
    dc.customer_id,
    dr.review_id,
    df.flight_id,
    dt.time_id,
    o.verified,
    o.type AS traveller_type,
    o.seat_type,
    o.seat_comfort,
    o.cabit_serv AS cabin_service,
    o.food,
    o.ground_service,
    o.wifi,
    o.money_value,
    o.recommended
FROM ba_review.dbo.original o
JOIN ba_review.dbo.dim_customer dc ON o.name = dc.customer_name
JOIN ba_review.dbo.dim_review dr ON o.id = dr.customer_id AND o.date_review = dr.date_review
JOIN ba_review.dbo.dim_flight df ON o.id = df.customer_id AND o.month_year_fly = df.month_year_fly
JOIN ba_review.dbo.dim_time dt ON CAST(o.date_review AS DATE) = dt.full_date;

-- Create indexes for better performance
CREATE NONCLUSTERED INDEX IX_fact_rating_customer_id ON ba_review.dbo.fact_rating (customer_id);
CREATE NONCLUSTERED INDEX IX_fact_rating_review_id ON ba_review.dbo.fact_rating (review_id);
CREATE NONCLUSTERED INDEX IX_fact_rating_flight_id ON ba_review.dbo.fact_rating (flight_id);
CREATE NONCLUSTERED INDEX IX_fact_rating_time_id ON ba_review.dbo.fact_rating (time_id);
