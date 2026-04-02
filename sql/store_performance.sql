SELECT
    store_id,
    region,
    ROUND(SUM(revenue), 2) AS total_revenue,
    SUM(units_sold) AS total_units,
    COUNT(*) AS transactions,
    RANK() OVER (ORDER BY SUM(revenue) DESC) AS revenue_rank
FROM sales
GROUP BY store_id, region
ORDER BY total_revenue DESC
