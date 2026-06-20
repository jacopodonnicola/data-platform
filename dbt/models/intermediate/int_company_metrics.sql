-- int_company_metrics.sql
SELECT
    o.ticker,
    o.name,
    o.sector,
    o.industry,
    o.market_capitalization,
    o.pe_ratio,
    o.eps,
    e.last_reported_eps,
    e.avg_surprise_percentage
FROM stg_overview o
LEFT JOIN (
    SELECT
        ticker,
        FIRST(reported_eps ORDER BY fiscal_date_ending DESC) AS last_reported_eps,
        AVG(surprise_percentage) AS avg_surprise_percentage
    FROM stg_earnings
    GROUP BY ticker
) e ON o.ticker = e.ticker