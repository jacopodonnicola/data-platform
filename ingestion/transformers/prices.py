import pandas as pd

def transform_prices(data: dict, ticker: str) -> pd.DataFrame:
    """
    Trasforma il JSON grezzo di TIME_SERIES_DAILY
    in un DataFrame pulito e tipizzato.
    """
    time_series = data['Time Series (Daily)']
    
    df = pd.DataFrame.from_dict(time_series, orient='index')
    
    # rinomina colonne
    df.columns = ['open', 'high', 'low', 'close', 'volume']
    
    # converti tipi
    df[['open', 'high', 'low', 'close']] = df[['open', 'high', 'low', 'close']].astype(float)
    df['volume'] = df['volume'].astype(int)
    
    # converti indice in datetime
    df.index = pd.to_datetime(df.index)
    df.index.name = 'date'
    
    # aggiungi ticker
    df['ticker'] = ticker
    
    # reset index
    df = df.reset_index()
    
    return df