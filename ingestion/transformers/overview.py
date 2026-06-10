import pandas as pd

def transform_overview(data: dict, ticker: str) -> pd.DataFrame:
    """
    Trasforma il JSON grezzo di OVERVIEW
    in un DataFrame pulito e tipizzato.
    """
    # colonne che ci interessano
    cols = [
        'Symbol', 'Name', 'Exchange', 'Currency', 'Country',
        'Sector', 'Industry', 'MarketCapitalization', 'EBITDA',
        'PERatio', 'EPS', 'Beta', '52WeekHigh', '52WeekLow',
        'DividendYield', 'ProfitMargin'
    ]

    df = pd.DataFrame([data])[cols]

    # colonne numeriche
    numeric_cols = [
        'MarketCapitalization', 'EBITDA', 'PERatio', 'EPS',
        'Beta', '52WeekHigh', '52WeekLow', 'DividendYield', 'ProfitMargin'
    ]

    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

    # aggiungi ticker
    df['ticker'] = ticker

    return df