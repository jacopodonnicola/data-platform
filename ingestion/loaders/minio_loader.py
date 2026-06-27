import io # per gestire i buffer in memoria
import json
import pandas as pd 
from minio import Minio # libreria ufficiale per interagire con MinIO, compatibile anche con AWS S3

def get_minio_client(endpoint: str, access_key: str, secret_key: str, secure: bool) -> Minio: 
    """
    Crea e restituisce un client MinIO, che ci permette di interagire con MinIO (caricare file, scaricare file, gestire bucket, ecc.).
    """
    return Minio(
        endpoint,
        access_key=access_key,
        secret_key=secret_key,
        secure=secure
    )


def save_json(client: Minio, bucket: str, object_path: str, data: dict) -> None:
    """
    Salva un dizionario come JSON su MinIO (layer raw/).
    """
    buffer = io.BytesIO(json.dumps(data).encode("utf-8"))
    client.put_object(
        bucket_name=bucket,
        object_name=object_path,
        data=buffer,
        length=buffer.getbuffer().nbytes,
        content_type="application/json"
    )
    

def save_parquet(client: Minio, bucket: str, object_path: str, df: pd.DataFrame) -> None:
    """
    Salva un DataFrame come Parquet su MinIO.
    """
    buffer = io.BytesIO() # Crea un buffer in memoria. Senza io.BytesIO() dovremmo salvare il Parquet su disco e poi caricarlo su MinIO — un passaggio inutile.
    df.to_parquet(buffer, index=False) # Salva il DataFrame come Parquet nel buffer. index=False per non includere l'indice del DataFrame nel file Parquet. 
    buffer.seek(0) # Riporta il puntatore del buffer all'inizio, altrimenti MinIO penserebbe che il buffer sia vuoto (perché è alla fine dopo la scrittura) e caricherebbe un file vuoto.

    client.put_object(  # Carica il buffer su MinIO come un oggetto. put_object è un metodo del client MinIO che accetta il nome del bucket, il percorso dell'oggetto, i dati da caricare, la lunghezza dei dati e il tipo di contenuto.
        bucket_name=bucket, # Il nome del bucket su MinIO dove vogliamo salvare il file Parquet.
        object_name=object_path, # Il percorso completo dell'oggetto su MinIO, che include il prefisso e il nome del file. Ad esempio, "prices/AAPL.parquet".
        data=buffer, # I dati da caricare, che in questo caso sono nel buffer in memoria. 
        length=buffer.getbuffer().nbytes, # Ottiene la lunghezza dei dati nel buffer. getbuffer() restituisce un oggetto memoryview che rappresenta il buffer, e nbytes restituisce la dimensione in byte del buffer.
        content_type="application/octet-stream" # Il tipo di contenuto è generico perché Parquet è un formato binario. In alternativa, potremmo usare "application/parquet" se vogliamo essere più specifici, ma "application/octet-stream" è ampiamente accettato per i file binari.
    )