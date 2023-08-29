import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
from read_trades import read_trades
from candlestick_formation import form_candlesticks
from calculate_ema import calculate_ema
from tests import (
    test_read_trades,
    test_form_candlesticks,
    test_calculate_ema,
    test_candlestick_values,
    test_ema_values,
)


def run_tests():
    """Запускает все тесты и выводит сообщение о результате."""
    test_read_trades()
    test_form_candlesticks()
    test_calculate_ema()
    test_candlestick_values()
    test_ema_values()
    print("Все тесты успешно пройдены!")


# Запускаем тесты
run_tests()

# Чтение данных
data = read_trades("prices.csv")

# Формирование свечных графиков
ohlc = form_candlesticks(data)
ohlc.to_csv("candlestick_data.csv")  # Сохранение данных свечных графиков

# Расчет EMA
ema_14 = calculate_ema(ohlc["close"], 14)
ema_14.to_csv("ema_14_data.csv")  # Сохранение данных EMA

# График
fig, ax = plt.subplots(figsize=(15, 7))
ohlc['Date_Num'] = mdates.date2num(ohlc.index.to_pydatetime())
candlestick_data = [tuple(x) for x in ohlc[['Date_Num', 'open', 'high', 'low', 'close']].values]
candlestick_ohlc(ax, candlestick_data, width=0.6, colorup='g', colordown='r')
ax.plot(ohlc.index, ema_14, label="14-period EMA", color="yellow")
ax.set_xlabel("Date")
ax.set_ylabel("Price")
ax.set_title("Candlestick with 14-period EMA")
ax.legend(loc='upper right')
plt.tight_layout()
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.xticks(rotation=45)
plt.savefig("output_chart.png")  # Сохранение графика в файл
plt.show()
