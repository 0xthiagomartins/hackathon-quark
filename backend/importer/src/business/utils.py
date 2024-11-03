from io import BytesIO
import pandas as pd


def read_csv_from_bytes(byte_data):
    byte_stream = BytesIO(byte_data)
    df = pd.read_csv(byte_stream)
    return df


def read_excel_from_bytes(byte_data):
    byte_stream = BytesIO(byte_data)
    df = pd.read_excel(byte_stream)
    return df
