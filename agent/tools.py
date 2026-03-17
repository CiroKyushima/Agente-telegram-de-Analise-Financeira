import yfinance as yf
import pandas as pd
from langchain.tools import tool
import requests
from datetime import datetime

@tool
def get_stock_data(symbol: str, period: str = "6mo"):
    """
    Busca dados históricos completos de uma ação.
    Retorna preços de fechamento, volume e preço atual.
    """
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period)

        if df.empty:
            return f"Erro: não foi possível encontrar dados para {symbol}"

        return {
            "close_prices": df["Close"].tolist(),
            "volumes": df["Volume"].tolist(),
            "current_price": float(df["Close"].iloc[-1])
        }

    except Exception as e:
        return f"Erro ao coletar dados: {str(e)}"

@tool
def calculate_sma(prices: list, window: int):
    """
    Calcula média móvel simples (SMA).
    """
    try:
        series = pd.Series(prices)

        sma = series.rolling(window=window).mean()

        return {
            "window": window,
            "value": float(sma.iloc[-1])
        }

    except Exception as e:
        return f"Erro no cálculo da SMA: {str(e)}"


@tool
def calculate_ema(prices: list, window: int):
    """
    Calcula média móvel exponencial (EMA).
    """
    try:
        series = pd.Series(prices)

        ema = series.ewm(span=window, adjust=False).mean()

        return {
            "window": window,
            "value": float(ema.iloc[-1])
        }

    except Exception as e:
        return f"Erro no cálculo da EMA: {str(e)}"

@tool
def calculate_rsi(prices: list, period: int = 14):
    """
    Calcula RSI (Relative Strength Index).
    """
    try:
        series = pd.Series(prices)

        delta = series.diff()

        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(period).mean()
        avg_loss = loss.rolling(period).mean()

        rs = avg_gain / avg_loss

        rsi = 100 - (100 / (1 + rs))

        value = float(rsi.iloc[-1])

        if value < 30:
            state = "SOBREVENDIDO"
        elif value > 70:
            state = "SOBRECOMPRADO"
        else:
            state = "NEUTRO"

        return {
            "rsi": value,
            "estado": state
        }

    except Exception as e:
        return f"Erro no cálculo do RSI: {str(e)}"


@tool
def calculate_macd(prices: list):
    """
    Calcula MACD (Moving Average Convergence Divergence).
    """
    try:
        series = pd.Series(prices)

        ema12 = series.ewm(span=12, adjust=False).mean()
        ema26 = series.ewm(span=26, adjust=False).mean()

        macd = ema12 - ema26
        signal = macd.ewm(span=9, adjust=False).mean()

        return {
            "macd": float(macd.iloc[-1]),
            "signal": float(signal.iloc[-1]),
            "histogram": float((macd - signal).iloc[-1])
        }

    except Exception as e:
        return f"Erro no cálculo do MACD: {str(e)}"

@tool
def calculate_volatility(prices: list):
    """
    Calcula volatilidade baseada no desvio padrão dos retornos.
    """
    try:
        series = pd.Series(prices)

        returns = series.pct_change()

        volatility = returns.std() * (252 ** 0.5)  # anualizada

        return {
            "volatility": float(volatility)
        }

    except Exception as e:
        return f"Erro ao calcular volatilidade: {str(e)}"

@tool
def calculate_bollinger_bands(prices: list, window: int = 20):
    """
    Calcula Bollinger Bands.
    """
    try:
        series = pd.Series(prices)

        sma = series.rolling(window).mean()

        std = series.rolling(window).std()

        upper_band = sma + (std * 2)
        lower_band = sma - (std * 2)

        return {
            "upper_band": float(upper_band.iloc[-1]),
            "middle_band": float(sma.iloc[-1]),
            "lower_band": float(lower_band.iloc[-1])
        }

    except Exception as e:
        return f"Erro no cálculo das Bollinger Bands: {str(e)}"

@tool
def detect_trend(price: float, sma20: float, sma50: float):
    """
    Detecta tendência baseada em médias móveis.
    """

    if price > sma20 > sma50:
        return "FORTE_ALTA"

    if price > sma20 and sma20 > sma50:
        return "ALTA"

    if price < sma20 < sma50:
        return "FORTE_BAIXA"

    if price < sma20:
        return "BAIXA"

    return "NEUTRO"

@tool
def generate_trading_signal(rsi_state: str, trend: str, macd_histogram: float):
    """
    Gera sinal de trading combinando múltiplos indicadores.
    """

    if rsi_state == "SOBREVENDIDO" and macd_histogram > 0 and trend in ["ALTA", "FORTE_ALTA"]:
        return "COMPRA"

    if rsi_state == "SOBRECOMPRADO" and macd_histogram < 0 and trend in ["BAIXA", "FORTE_BAIXA"]:
        return "VENDA"

    return "AGUARDAR"

@tool
def calculate_sharpe_ratio(prices: list, risk_free_rate: float = 0.02):
    """
    Calcula o Sharpe Ratio para avaliar retorno ajustado ao risco.
    """
    try:

        series = pd.Series(prices)

        returns = series.pct_change().dropna()

        excess_returns = returns - (risk_free_rate / 252)

        sharpe = (excess_returns.mean() / excess_returns.std()) * (252 ** 0.5)

        return {
            "sharpe_ratio": float(sharpe)
        }

    except Exception as e:
        return f"Erro no cálculo do Sharpe Ratio: {str(e)}"
    
@tool
def calculate_max_drawdown(prices: list):
    """
    Calcula o Maximum Drawdown (maior perda histórica).
    """
    try:

        series = pd.Series(prices)

        cumulative_max = series.cummax()

        drawdown = (series - cumulative_max) / cumulative_max

        max_drawdown = drawdown.min()

        return {
            "max_drawdown": float(max_drawdown)
        }

    except Exception as e:
        return f"Erro no cálculo do Drawdown: {str(e)}"
    
@tool
def calculate_atr(high_prices: list, low_prices: list, close_prices: list, period: int = 14):
    """
    Calcula o ATR (Average True Range).
    """

    try:

        high = pd.Series(high_prices)
        low = pd.Series(low_prices)
        close = pd.Series(close_prices)

        tr1 = high - low
        tr2 = (high - close.shift()).abs()
        tr3 = (low - close.shift()).abs()

        true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

        atr = true_range.rolling(period).mean()

        return {
            "atr": float(atr.iloc[-1])
        }

    except Exception as e:
        return f"Erro no cálculo do ATR: {str(e)}"
    
@tool
def analyze_volume_trend(volumes: list):
    """
    Analisa tendência de volume de negociação.
    """

    try:

        series = pd.Series(volumes)

        volume_ma20 = series.rolling(20).mean()

        current_volume = series.iloc[-1]

        avg_volume = volume_ma20.iloc[-1]

        if current_volume > avg_volume:
            trend = "VOLUME_ALTO"
        else:
            trend = "VOLUME_BAIXO"

        return {
            "volume_atual": float(current_volume),
            "media_volume_20": float(avg_volume),
            "tendencia_volume": trend
        }

    except Exception as e:
        return f"Erro na análise de volume: {str(e)}"
    
@tool
def detect_market_regime(prices: list):
    """
    Detecta regime de mercado (Bull, Bear ou Sideways).
    """

    try:

        series = pd.Series(prices)

        sma50 = series.rolling(50).mean()
        sma200 = series.rolling(200).mean()

        current_price = series.iloc[-1]

        sma50_last = sma50.iloc[-1]
        sma200_last = sma200.iloc[-1]

        if current_price > sma50_last > sma200_last:
            regime = "BULL_MARKET"

        elif current_price < sma50_last < sma200_last:
            regime = "BEAR_MARKET"

        else:
            regime = "SIDEWAYS"

        return {
            "market_regime": regime
        }

    except Exception as e:
        return f"Erro na detecção de regime: {str(e)}"
    
@tool
def analyze_market_news(symbol: str):
    """
    Busca notícias recentes, menções em redes sociais e analisa o sentimento do mercado
    relacionado a uma ação específica.
    """

    try:

        ticker = yf.Ticker(symbol)

        news = ticker.news

        if not news:
            return {
                "news_found": 0,
                "sentiment": "NEUTRO",
                "summary": "Nenhuma notícia recente encontrada."
            }

        headlines = []
        positive_words = ["growth", "profit", "upgrade", "record", "strong"]
        negative_words = ["loss", "downgrade", "drop", "lawsuit", "decline"]

        score = 0

        for item in news[:10]:

            title = item.get("title", "")

            headlines.append(title)

            title_lower = title.lower()

            for word in positive_words:
                if word in title_lower:
                    score += 1

            for word in negative_words:
                if word in title_lower:
                    score -= 1

        if score > 2:
            sentiment = "POSITIVO"
        elif score < -2:
            sentiment = "NEGATIVO"
        else:
            sentiment = "NEUTRO"

        return {
            "symbol": symbol,
            "news_found": len(headlines),
            "sentiment": sentiment,
            "recent_headlines": headlines,
            "analysis_time": datetime.now().isoformat()
        }

    except Exception as e:
        return f"Erro ao analisar notícias: {str(e)}"