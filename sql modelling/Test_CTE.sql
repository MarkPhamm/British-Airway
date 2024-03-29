SELECT 
ROW_NUMBER() OVER(ORDER BY date_review) as rating_id,
ROW_NUMBER() OVER(Partition by customer_name order by customer_name) as customer_Id
FROM ba_review.dbo.original