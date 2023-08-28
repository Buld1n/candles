def calculate_ema(data, period):
    """Расчет экспоненциального скользящего среднего (EMA) для заданного периода."""
    alpha = 2 / (period + 1)
    return data.ewm(alpha=alpha, adjust=False).mean()
