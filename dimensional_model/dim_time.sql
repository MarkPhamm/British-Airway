-- Check if the table exists and drop it if it does
IF OBJECT_ID('ba_review.dbo.dim_time', 'U') IS NOT NULL
BEGIN
    DROP TABLE ba_review.dbo.dim_time;
END
GO

-- Create the dim_time table
CREATE TABLE ba_review.dbo.dim_time (
    time_id INT IDENTITY(1,1) PRIMARY KEY,
    full_date DATE NOT NULL,
    year INT NOT NULL,
    quarter TINYINT NOT NULL,
    month TINYINT NOT NULL,
    day TINYINT NOT NULL,
    week TINYINT NOT NULL,
    day_of_week TINYINT NOT NULL,
    day_name NVARCHAR(10) NOT NULL,
    month_name NVARCHAR(10) NOT NULL,
    is_weekend BIT NOT NULL
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
    DATEPART(ISO_WEEK, dt) AS week,
    DATEPART(WEEKDAY, dt) AS day_of_week,
    FORMAT(dt, 'dddd') AS day_name,
    FORMAT(dt, 'MMMM') AS month_name,
    CASE WHEN DATEPART(WEEKDAY, dt) IN (6, 7) THEN 1 ELSE 0 END AS is_weekend
FROM
    DateRange
OPTION (MAXRECURSION 0);

-- Create indexes for faster querying
CREATE NONCLUSTERED INDEX IX_dim_time_full_date ON ba_review.dbo.dim_time (full_date);
CREATE NONCLUSTERED INDEX IX_dim_time_year ON ba_review.dbo.dim_time (year);
CREATE NONCLUSTERED INDEX IX_dim_time_month ON ba_review.dbo.dim_time (month, year);
CREATE NONCLUSTERED INDEX IX_dim_time_day ON ba_review.dbo.dim_time (day, month, year);
