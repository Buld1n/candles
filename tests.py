import os
import pandas as pd
import numpy as np
from read_trades import read_trades
from candlestick_formation import form_candlesticks
from calculate_ema import calculate_ema

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'prices.csv')


def test_read_trades():
    data = read_trades(file_path)
    assert isinstance(data, pd.DataFrame), "Output should be a DataFrame"
    assert "TS" in data.columns, "TS column missing"
    assert "PRICE" in data.columns, "PRICE column missing"


def test_form_candlesticks():
    data = read_trades(file_path)
    ohlc = form_candlesticks(data)
    assert isinstance(ohlc, pd.DataFrame), "Output should be a DataFrame"
    for col in ["open", "high", "low", "close"]:
        assert col in ohlc.columns, f"{col} column missing"


def test_candlestick_values():
    data = read_trades(file_path)
    ohlc = form_candlesticks(data)
    # Проверка, что значение 'open' равно первому значению 'PRICE' в интервале
    assert ohlc["open"].iloc[0] == data["PRICE"].iloc[0], "Open value mismatch"
    # Проверка, что значение 'close' равно последнему значению 'PRICE' в интервале
    last_value_before_next_ohlc = data[data.index < ohlc.index[1]]["PRICE"].iloc[-1]
    assert ohlc["close"].iloc[0] == last_value_before_next_ohlc, "Close value mismatch"
    # Проверка, что значение 'high' действительно максимальное в интервале
    assert (
        ohlc["high"].iloc[0] == data["PRICE"][data.index < ohlc.index[1]].max()
    ), "High value mismatch"
    # Проверка, что значение 'low' действительно минимальное в интервале
    assert (
        ohlc["low"].iloc[0] == data["PRICE"][data.index < ohlc.index[1]].min()
    ), "Low value mismatch"


def test_calculate_ema():
    data = read_trades(file_path)
    ohlc = form_candlesticks(data)
    ema_14 = calculate_ema(ohlc["close"], 14)
    assert isinstance(ema_14, pd.Series), "Output should be a Series"
    assert len(ema_14) == len(ohlc), "EMA length should match OHLC length"


def test_ema_values():
    data = read_trades(file_path)
    ohlc = form_candlesticks(data)
    ema_14 = calculate_ema(ohlc["close"], 14)
    # Проверка корректности расчета EMA
    alpha = 2 / (14 + 1)
    expected_ema = (ohlc["close"].iloc[14] - ema_14.iloc[13]) * alpha + ema_14.iloc[13]
    assert np.isclose(
        ema_14.iloc[14], expected_ema, atol=1e-2
    ), "Subsequent EMA value mismatch"
