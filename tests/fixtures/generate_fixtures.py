import pandas as pd
import os

os.makedirs('tests/fixtures', exist_ok=True)

# prices
pd.DataFrame({
    'date': pd.date_range('2026-01-01', periods=10),
    'open': [100.0] * 10,
    'high': [105.0] * 10,
    'low': [95.0] * 10,
    'close': [102.0] * 10,
    'volume': [1000000] * 10,
    'ticker': ['AAPL'] * 10
}).to_parquet('tests/fixtures/prices.parquet', index=False)

# overview
pd.DataFrame({
    'Symbol': ['AAPL'],
    'Name': ['Apple Inc.'],
    'Exchange': ['NASDAQ'],
    'Currency': ['USD'],
    'Country': ['USA'],
    'Sector': ['Technology'],
    'Industry': ['Consumer Electronics'],
    'MarketCapitalization': [3000000000000],
    'EBITDA': [130000000000],
    'PERatio': [28.5],
    'EPS': [6.5],
    'Beta': [1.2],
    '52WeekHigh': [200.0],
    '52WeekLow': [150.0],
    'DividendYield': [0.005],
    'ProfitMargin': [0.25],
    'ticker': ['AAPL']
}).to_parquet('tests/fixtures/overview.parquet', index=False)

# earnings
pd.DataFrame({
    'fiscalDateEnding': pd.date_range('2025-01-01', periods=4, freq='QE'),
    'reportedDate': pd.date_range('2025-02-01', periods=4, freq='QE'),
    'reportedEPS': [1.5, 1.8, 2.0, 2.2],
    'estimatedEPS': [1.4, 1.7, 1.9, 2.1],
    'surprise': [0.1, 0.1, 0.1, 0.1],
    'surprisePercentage': [7.1, 5.9, 5.3, 4.8],
    'reportTime': ['post-market'] * 4,
    'ticker': ['AAPL'] * 4
}).to_parquet('tests/fixtures/earnings.parquet', index=False)

print("Fixtures generate correttamente")