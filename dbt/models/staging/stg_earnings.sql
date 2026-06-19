SELECT
    ticker,
    "fiscalDateEnding" AS fiscal_date_ending,
    "reportedDate" AS reported_date,
    "reportedEPS" AS reported_eps,
    "estimatedEPS" AS estimated_eps,
    "surprise" AS surprise,
    "surprisePercentage" AS surprise_percentage,
    "reportTime" AS report_time
FROM read_parquet('s3://staging/earnings/*.parquet')