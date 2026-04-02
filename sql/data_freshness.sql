SELECT
    store_id,
    ROUND(AVG(data_freshness_lag_days), 1) AS avg_lag_days,
    MAX(data_freshness_lag_days) AS max_lag_days,
    CASE
        WHEN AVG(data_freshness_lag_days) <= 2 THEN 'Fresh'
        WHEN AVG(data_freshness_lag_days) <= 5 THEN 'Stale'
        ELSE 'Critical'
    END AS freshness_status
FROM sales
GROUP BY store_id
ORDER BY avg_lag_days DESC
