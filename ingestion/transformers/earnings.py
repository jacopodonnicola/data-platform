import pandas as pd

def transform_earnings(data: dict, ticker: str) -> pd.DataFrame:
    """
    Trasforma il JSON grezzo di EARNINGS
    in un DataFrame pulito e tipizzato.
    """
    df = pd.DataFrame(data['quarterlyEarnings'])

    # colonne numeriche
    numeric_cols = [
        'reportedEPS', 'estimatedEPS', 'surprise', 'surprisePercentage'
    ]

    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

    # converti date
    df['fiscalDateEnding'] = pd.to_datetime(df['fiscalDateEnding'])
    df['reportedDate'] = pd.to_datetime(df['reportedDate'])

    # aggiungi ticker
    df['ticker'] = ticker

    return df
