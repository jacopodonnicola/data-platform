SELECT
    ticker,
    name,
    sector,
    industry,
    market_capitalization,
    pe_ratio,
    eps,
    last_reported_eps,
    avg_surprise_percentage
FROM {{ ref('int_company_metrics') }}