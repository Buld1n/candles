import os
import pandas as pd
import numpy as np
from read_trades import read_trades
from candlestick_formation import form_candlesticks
from calculate_ema import calculate_ema

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'prices.csv')


def test_read_trades():
    """
    Тестирование функции read_trades:
    - Проверка наличия столбцов 'TS' и 'PRICE'
    - Проверка формата вывода (DataFrame)
    """
    data = read_trades(file_path)
    assert isinstance(data, pd.DataFrame), "Output should be a DataFrame"
    assert "TS" in data.columns, "TS column missing"
    assert "PRICE" in data.columns, "PRICE column missing"


def test_form_candlesticks():
    """
    Тестирование функции form_candlesticks:
    - Проверка формата вывода (DataFrame)
    - Проверка наличия необходимых столбцов (open, high, low, close)
    """
    data = read_trades(file_path)
    ohlc = form_candlesticks(data)
    assert isinstance(ohlc, pd.DataFrame), "Output should be a DataFrame"
    for col in ["open", "high", "low", "close"]:
        assert col in ohlc.columns, f"{col} column missing"


def test_candlestick_values():
    """
    Тестирование значений свечных графиков:
    - Проверка корректности значений open, close, high, low для первого интервала времени
    """
    data = read_trades(file_path)
    ohlc = form_candlesticks(data)
    assert ohlc["open"].iloc[0] == data["PRICE"].iloc[0], "Open value mismatch"
    last_value_before_next_ohlc = data[data.index < ohlc.index[1]]["PRICE"].iloc[-1]
    assert ohlc["close"].iloc[0] == last_value_before_next_ohlc, "Close value mismatch"
    assert (
        ohlc["high"].iloc[0] == data["PRICE"][data.index < ohlc.index[1]].max()
    ), "High value mismatch"
    assert (
        ohlc["low"].iloc[0] == data["PRICE"][data.index < ohlc.index[1]].min()
    ), "Low value mismatch"


def test_calculate_ema():
    """
    Тестирование функции calculate_ema:
    - Проверка формата вывода (pd.Series)
    - Проверка согласованности длины EMA и OHLC
    """
    data = read_trades(file_path)
    ohlc = form_candlesticks(data)
    ema_14 = calculate_ema(ohlc["close"], 14)
    assert isinstance(ema_14, pd.Series), "Output should be a Series"
    assert len(ema_14) == len(ohlc), "EMA length should match OHLC length"


def test_ema_values():
    """
    Тестирование корректности значений EMA:
    - Проверка первого рассчитанного значения EMA
    - Проверка последующих значений EMA на основе формулы расчета
    """
    data = read_trades(file_path)
    ohlc = form_candlesticks(data)
    ema_14 = calculate_ema(ohlc["close"], 14)
    alpha = 2 / (14 + 1)
    expected_ema = (ohlc["close"].iloc[14] - ema_14.iloc[13]) * alpha + ema_14.iloc[13]
    assert np.isclose(
        ema_14.iloc[14], expected_ema, atol=1e-2
    ), "Subsequent EMA value mismatch"
