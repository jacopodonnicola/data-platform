SELECT
    ticker,
    date,
    open,
    high,
    low,
    close,
    volume
FROM read_parquet('s3://staging/prices/*.parquet')