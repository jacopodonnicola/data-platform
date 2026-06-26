SELECT
    ticker,
    "Symbol" AS symbol,
    "Name" AS name,
    "Exchange" AS exchange,
    "Currency" AS currency,
    "Country" AS country,
    "Sector" AS sector,
    "Industry" AS industry,
    "MarketCapitalization" AS market_capitalization,
    "EBITDA" AS ebitda,
    "PERatio" AS pe_ratio,
    "EPS" AS eps,
    "Beta" AS beta,
    "52WeekHigh" AS week_52_high,
    "52WeekLow" AS week_52_low,
    "DividendYield" AS dividend_yield,
    "ProfitMargin" AS profit_margin
FROM read_parquet('{{ env_var("OVERVIEW_PATH", "s3://staging/overview/*.parquet") }}')
