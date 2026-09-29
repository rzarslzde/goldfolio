SELECT
    id,
    user_id,
    symbol,
    quantity,
    avg_buy_price,
    current_price,
    (quantity * current_price) AS market_value
FROM holdings
ORDER BY market_value DESC
LIMIT 100;
