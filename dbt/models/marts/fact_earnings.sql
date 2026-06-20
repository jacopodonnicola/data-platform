SELECT
    ticker,
    fiscal_date_ending,
    reported_date,
    reported_eps,
    estimated_eps,
    surprise,
    surprise_percentage,
    report_time
FROM {{ ref('stg_earnings') }}