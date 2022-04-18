import pandas as pd


def format_date(date_string, bytestring_key):
    format = '%Y-%m-%d'
    pandas_datetime = pd.to_datetime(date_string, format=format, utc=True)
    return pd.Series(name=bytestring_key, data=pandas_datetime)
