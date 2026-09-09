-- Customer Behavior & Sales Analytics Dashboard
-- Fresh business questions and SQL logic for the new project.

-- 1. Which categories combine scale with high order value?
SELECT category,
       COUNT(*) AS purchases,
       ROUND(SUM(purchase_amount_usd), 2) AS revenue,
       ROUND(AVG(purchase_amount_usd), 2) AS average_order_value
FROM customer_behavior_clean
GROUP BY category
ORDER BY revenue DESC;

-- 2. Does subscription status correlate with repeat behavior?
SELECT subscription_status,
       COUNT(*) AS customers,
       ROUND(AVG(purchase_amount_usd), 2) AS average_order_value,
       ROUND(AVG(previous_purchases), 1) AS average_previous_purchases,
       ROUND(AVG(CASE WHEN previous_purchases >= 10 THEN 1.0 ELSE 0 END), 3) AS repeat_rate
FROM customer_behavior_clean
GROUP BY subscription_status
ORDER BY repeat_rate DESC;

-- 3. Which customer segments should receive different messages?
SELECT customer_segment,
       COUNT(*) AS customers,
       ROUND(SUM(purchase_amount_usd), 2) AS revenue,
       ROUND(AVG(purchase_amount_usd), 2) AS average_order_value,
       ROUND(AVG(CASE WHEN discount_flag THEN 1.0 ELSE 0 END), 3) AS discount_rate
FROM customer_behavior_clean
GROUP BY customer_segment
ORDER BY revenue DESC;

-- 4. Which shipping options are associated with higher value baskets?
SELECT shipping_type,
       COUNT(*) AS purchases,
       ROUND(AVG(purchase_amount_usd), 2) AS average_order_value,
       ROUND(AVG(review_rating), 2) AS average_rating
FROM customer_behavior_clean
GROUP BY shipping_type
ORDER BY average_order_value DESC;

-- 5. Which age bands are strongest revenue opportunities?
SELECT age_band,
       COUNT(*) AS purchases,
       ROUND(SUM(purchase_amount_usd), 2) AS revenue,
       ROUND(AVG(purchase_amount_usd), 2) AS average_order_value
FROM customer_behavior_clean
GROUP BY age_band
ORDER BY revenue DESC;
