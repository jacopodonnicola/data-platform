SELECT
    ticker,
    date,
    open,
    high,
    low,
    close,
    volume
FROM read_parquet('{{ env_var("PRICES_PATH", "s3://staging/prices/*.parquet") }}')
