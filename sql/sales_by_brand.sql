SELECT
    brand,
    COUNT(*) AS transactions,
    SUM(units_sold) AS total_units,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(AVG(price), 2) AS avg_price
FROM sales
GROUP BY brand
ORDER BY total_revenue DESC
