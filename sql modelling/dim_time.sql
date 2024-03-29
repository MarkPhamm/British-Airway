SELECT 
    date_review, 
    DATEPART(YEAR, date_review) as year,
    DATEPART(QUARTER, date_review) as quarter,
    DATEPART(MONTH, date_review) as month_num,
    FORMAT(date_review, 'MMMM') as month,
    DATEPART(ISO_WEEK, date_review) as week,
    DATENAME(WEEKDAY, date_review) as day_of_week
FROM ba_review.dbo.original