def form_candlesticks(data, interval="5T"):
    """Преобразование данных в свечные графики на основе заданного временного интервала."""
    data.set_index("TS", inplace=True)
    ohlc = data["PRICE"].resample(interval).ohlc()
    return ohlc
