import pandas as pd


def read_trades(file_path):
    """Чтение данных из CSV и преобразование столбца Timestamp в datetime."""
    data = pd.read_csv(file_path)
    data["TS"] = pd.to_datetime(data["TS"])
    return data
