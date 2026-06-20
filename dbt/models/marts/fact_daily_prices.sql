SELECT
    ticker,
    date,
    open,
    high,
    low,
    close,
    volume
FROM {{ ref('stg_prices') }}