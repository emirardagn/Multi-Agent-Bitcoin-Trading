import yaml
import yfinance as yf
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime, timedelta
from crewai.tools import tool

parameters = yaml.safe_load(open('src/bitcointrading/config/parameters.yaml'))["technical_indicators"]


def calculate_ema(df, periods):
    """Calculate Exponential Moving Average for given periods"""
    emas = {}
    for period in periods:
        emas[f'EMA{period}'] = df['Close'].ewm(span=period, adjust=False).mean()
    return emas

def calculate_macd(df, fast=parameters["MACD_FAST"], slow=parameters["MACD_SLOW"], signal=parameters["MACD_SIGNAL"]):
    """Calculate MACD (Moving Average Convergence Divergence)"""
    exp1 = df['Close'].ewm(span=fast, adjust=False).mean()
    exp2 = df['Close'].ewm(span=slow, adjust=False).mean()
    macd = exp1 - exp2
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    histogram = macd - signal_line
    return macd, signal_line, histogram

def calculate_rsi(df, period=parameters["RSI_PERIOD"]):
    """Calculate Relative Strength Index"""
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_bollinger_bands(df, period=parameters["BOLLINGER_PERIOD"], std_dev=parameters["BOLLINGER_STD_DEV"]):
    """Calculate Bollinger Bands"""
    middle = df['Close'].rolling(window=period).mean()
    std = df['Close'].rolling(window=period).std()
    upper = middle + (std * std_dev)
    lower = middle - (std * std_dev)
    bandwidth = (upper - lower) / middle
    return middle, upper, lower, bandwidth

def calculate_stochastic(df, k_period=parameters["STOCHASTIC_K_PERIOD"], d_period=parameters["STOCHASTIC_D_PERIOD"]):
    """Calculate Stochastic Oscillator"""
    lowest = df['Low'].rolling(window=k_period).min()
    highest = df['High'].rolling(window=k_period).max()
    k = 100 * ((df['Close'] - lowest) / (highest - lowest))
    d = k.rolling(window=d_period).mean()
    return k, d

def calculate_vwap(df):
    """Calculate Volume Weighted Average Price"""
    return (df['Volume'] * (df['High'] + df['Low'] + df['Close']) / 3).cumsum() / df['Volume'].cumsum()

def calculate_atr(df, period=parameters["ATR_PERIOD"]):
    """Calculate Average True Range"""
    high_low = df['High'] - df['Low']
    high_close = np.abs(df['High'] - df['Close'].shift())
    low_close = np.abs(df['Low'] - df['Close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)
    return true_range.rolling(window=period).mean()

def calculate_adx(df, period=parameters["ADX_PERIOD"]):
    """Calculate Average Directional Index"""
    plus_dm = df['High'].diff()
    minus_dm = df['Low'].diff()
    plus_dm[plus_dm < 0] = 0
    minus_dm[minus_dm > 0] = 0
    
    tr = calculate_atr(df, period)
    plus_di = 100 * (plus_dm.rolling(window=period).mean() / tr)
    minus_di = 100 * (minus_dm.rolling(window=period).mean() / tr)
    dx = 100 * np.abs(plus_di - minus_di) / (plus_di + minus_di)
    return dx.rolling(window=period).mean()

def calculate_obv(df):
    """Calculate On-Balance Volume"""
    return (np.sign(df['Close'].diff()) * df['Volume']).cumsum()

def calculate_parabolic_sar(df, acc_factor=parameters["PARABOLIC_SAR_ACC_FACTOR"], max_acc_factor=parameters["PARABOLIC_SAR_MAX_ACC_FACTOR"]):
    """Calculate Parabolic SAR"""
    sar = df['Close'].copy()
    trend = 1
    af = acc_factor
    
    for i in range(2, len(df)):
        if trend == 1:
            sar.iloc[i] = sar.iloc[i-1] + af * (df['High'].iloc[i-1] - sar.iloc[i-1])
            if df['Low'].iloc[i] < sar.iloc[i]:
                trend = -1
                af = acc_factor
                sar.iloc[i] = df['High'].iloc[i-1]
            else:
                if df['High'].iloc[i] > df['High'].iloc[i-1]:
                    af = min(af + acc_factor, max_acc_factor)
        else:
            sar.iloc[i] = sar.iloc[i-1] - af * (sar.iloc[i-1] - df['Low'].iloc[i-1])
            if df['High'].iloc[i] > sar.iloc[i]:
                trend = 1
                af = acc_factor
                sar.iloc[i] = df['Low'].iloc[i-1]
            else:
                if df['Low'].iloc[i] < df['Low'].iloc[i-1]:
                    af = min(af + acc_factor, max_acc_factor)
    return sar

def find_support_resistance(df, window=parameters["SUPPORT_RESISTANCE_WINDOW"], num_levels=parameters["SUPPORT_RESISTANCE_NUM_LEVELS"]):
    """Find support and resistance levels using more sophisticated methods"""
    df = df.copy()
    
    # Calculate pivot points with Fibonacci levels
    pivot = (df['High'].iloc[-1] + df['Low'].iloc[-1] + df['Close'].iloc[-1]) / 3
    r1 = 2 * pivot - df['Low'].iloc[-1]
    s1 = 2 * pivot - df['High'].iloc[-1]
    r2 = pivot + (df['High'].iloc[-1] - df['Low'].iloc[-1])
    s2 = pivot - (df['High'].iloc[-1] - df['Low'].iloc[-1])
    
    # Fibonacci levels
    fib_levels = [0.236, 0.382, 0.5, 0.618, 0.786]
    price_range = df['High'].iloc[-1] - df['Low'].iloc[-1]
    fib_resistance = [df['High'].iloc[-1] - level * price_range for level in fib_levels]
    fib_support = [df['Low'].iloc[-1] + level * price_range for level in fib_levels]
    
    # Find local maxima and minima with rolling window
    df['is_local_max'] = df['High'].rolling(window=window, center=True).max() == df['High']
    df['is_local_min'] = df['Low'].rolling(window=window, center=True).min() == df['Low']
    
    # Get support levels (local minima)
    support_levels = df[df['is_local_min']]['Low'].tail(num_levels).values
    
    # Get resistance levels (local maxima)
    resistance_levels = df[df['is_local_max']]['High'].tail(num_levels).values
    
    # Combine all levels
    support_levels = np.append(support_levels, [s1, s2] + fib_support)
    resistance_levels = np.append(resistance_levels, [r1, r2] + fib_resistance)
    
    # Remove duplicates and sort
    support_levels = np.unique(support_levels)
    resistance_levels = np.unique(resistance_levels)
    
    # Sort and get the most recent levels
    support_levels = np.sort(support_levels)[-num_levels:]
    resistance_levels = np.sort(resistance_levels)[:num_levels]
    
    return support_levels, resistance_levels

#Main Function That Calculates All Indicators -> tool for trading
@tool("Calculate technical indicators for BTC-USD")
def CALCULATE_INDICATORS() -> dict:
    """Useful for calculating various technical indicators for Bitcoin trading analysis.
    Returns a comprehensive report including:
    - Moving averages (EMA)
    - MACD
    - RSI
    - Bollinger Bands
    - Stochastic Oscillator
    - VWAP
    - ATR
    - ADX
    - OBV
    - Parabolic SAR
    - Support and Resistance levels
    
    Args:
        days (int): Number of days to analyze (default from parameters)
    
    Returns:
        dict: A dictionary containing all calculated indicators and their values"""
    days: int = parameters["DAYS"]
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    btc = yf.Ticker("BTC-USD")
    df = btc.history(start=start_date, end=end_date, interval="1d")
    df = df.reset_index()
    
    # Standard periods for indicators
    ema_periods = parameters["EMA_PERIODS"]
    
    # Calculate all indicators
    emas = calculate_ema(df, ema_periods)
    macd, signal_line, histogram = calculate_macd(df)
    rsi = calculate_rsi(df)
    bb_middle, bb_upper, bb_lower, bb_bandwidth = calculate_bollinger_bands(df)
    stoch_k, stoch_d = calculate_stochastic(df)
    vwap = calculate_vwap(df)
    atr = calculate_atr(df)
    adx = calculate_adx(df)
    obv = calculate_obv(df)
    sar = calculate_parabolic_sar(df)
    
    # Find support and resistance levels
    support, resistance = find_support_resistance(df)
    
    # Prepare the report
    report = {
        "symbol": "BTC-USD",
        "analysis_period": f"Last {days} days",
        "current_price": df['Close'].iloc[-1],
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "indicators": {
            "EMAs": {f"EMA{period}": emas[f'EMA{period}'].iloc[-1] for period in ema_periods},
            "MACD": {
                "value": macd.iloc[-1],
                "signal_line": signal_line.iloc[-1],
                "histogram": histogram.iloc[-1]
            },
            "RSI": rsi.iloc[-1],
            "Bollinger_Bands": {
                "upper": bb_upper.iloc[-1],
                "middle": bb_middle.iloc[-1],
                "lower": bb_lower.iloc[-1],
                "bandwidth": bb_bandwidth.iloc[-1]
            },
            "Stochastic_Oscillator": {
                "%K": stoch_k.iloc[-1],
                "%D": stoch_d.iloc[-1]
            },
            "VWAP": vwap.iloc[-1],
            "ATR": atr.iloc[-1],
            "ADX": adx.iloc[-1],
            "OBV": obv.iloc[-1],
            "Parabolic_SAR": sar.iloc[-1],
            "Support_Levels": support.tolist(),
            "Resistance_Levels": resistance.tolist()
        }
    }
    
    return report
