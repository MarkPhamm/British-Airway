IF OBJECT_ID('ba_review.dbo.dim_time', 'U') IS NOT NULL
BEGIN
    DROP TABLE ba_review.dbo.dim_time;
END
GO

-- Create the dim_time table
CREATE TABLE ba_review.dbo.dim_time (
    time_id INT IDENTITY(1,1) PRIMARY KEY,
    full_date DATE,
    year INT,
    quarter INT,
    month INT,
    day INT,
    week INT,
    day_of_week INT,
    day_name VARCHAR(20),
    month_name VARCHAR(20),
    is_weekend BIT
);

-- Populating the dim_time table with data from 2010 to the current date
DECLARE @StartDate DATE = '2010-01-01';
DECLARE @EndDate DATE = GETDATE();

WITH DateRange AS (
    SELECT @StartDate AS dt
    UNION ALL
    SELECT DATEADD(DAY, 1, dt)
    FROM DateRange
    WHERE dt < @EndDate
)

INSERT INTO ba_review.dbo.dim_time (full_date, year, quarter, month, day, week, day_of_week, day_name, month_name, is_weekend)
SELECT
    dt AS full_date,
    YEAR(dt) AS year,
    DATEPART(QUARTER, dt) AS quarter,
    MONTH(dt) AS month,
    DAY(dt) AS day,
    DATEPART(WEEK, dt) AS week,
    DATEPART(WEEKDAY, dt) AS day_of_week,
    DATENAME(WEEKDAY, dt) AS day_name,
    DATENAME(MONTH, dt) AS month_name,
    CASE WHEN DATEPART(WEEKDAY, dt) IN (1, 7) THEN 1 ELSE 0 END AS is_weekend
FROM
    DateRange
OPTION (MAXRECURSION 0);

-- Optional: Create indexes for faster querying
CREATE INDEX idx_dim_time_full_date ON ba_review.dbo.dim_time (full_date);
CREATE INDEX idx_dim_time_year ON ba_review.dbo.dim_time (year);
CREATE INDEX idx_dim_time_month ON ba_review.dbo.dim_time (month);
CREATE INDEX idx_dim_time_day ON ba_review.dbo.dim_time (day);
