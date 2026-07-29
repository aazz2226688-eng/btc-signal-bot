# -*- coding: utf-8 -*-
import ccxt
import pandas as pd
import numpy as np
from ta.trend import MACD, EMAIndicator
from scipy.signal import argrelextrema
import requests

# ==================================================
# 🔧 設定區
# ==================================================
TELEGRAM_TOKEN = "8666112168:AAGaaRW0D5BTFgbItsMEhmeGzdkZhQnWvv8"
TELEGRAM_CHAT_ID = "997991682"
# ==================================================

def send_telegram(message):
    """發送訊息到 Telegram 手機"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": message}, timeout=5)
    except Exception as e:
        print(f"發送 Telegram 失敗: {e}")

def analyze_btc():
    """分析 BTC"""
    print(f"執行時間: {pd.Timestamp.now()}")

    try:
        exchange = ccxt.binance()
        ohlcv = exchange.fetch_ohlcv('BTC/USDT', timeframe='4h', limit=650)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        print(f"✅ 成功抓取 {len(df)} 根 K 線")
    except Exception as e:
        print(f"❌ 抓取數據失敗: {e}")
        return

    # 計算均線與 MACD
    for period in [36, 72, 144, 169, 288, 576]:
        df[f'ema_{period}'] = EMAIndicator(close=df['close'], window=period).ema_indicator()

    macd = MACD(close=df['close'])
    df['macd'] = macd.macd()
    df['signal'] = macd.macd_signal()
    df['histogram'] = macd.macd_diff()

    # 尋找 W底 和 M頂
    def find_pivot_lows(df, order=5):
        lows = df['low'].values
        return argrelextrema(lows, np.less, order=order)[0]

    def find_pivot_highs(df, order=5):
        highs = df['high'].values
        return argrelextrema(highs, np.greater, order=order)[0]

    recent_df = df.tail(40)
    pivot_lows = find_pivot_lows(recent_df, order=3)
    pivot_highs = find_pivot_highs(recent_df, order=3)

    # 檢查 W底
    w_pattern = False
    if len(pivot_lows) >= 2:
        idx1 = pivot_lows[-2]
        idx2 = pivot_lows[-1]
        if recent_df.iloc[idx2]['low'] > recent_df.iloc[idx1]['low']:
            ema144_val = recent_df.iloc[-1]['ema_144']
            low1_val = recent_df.iloc[idx1]['low']
            low2_val = recent_df.iloc[idx2]['low']
            if (abs(low1_val - ema144_val) / ema144_val < 0.10) or (abs(low2_val - ema144_val) / ema144_val < 0.10):
                w_pattern = True

    # 檢查 M頂
    m_pattern = False
    if len(pivot_highs) >= 2:
        idx1 = pivot_highs[-2]
        idx2 = pivot_highs[-1]
        if recent_df.iloc[idx2]['high'] < recent_df.iloc[idx1]['high']:
 # -*- coding: utf-8 -*-
import ccxt
import pandas as pd
import numpy as np
from ta.trend import MACD, EMAIndicator
from scipy.signal import argrelextrema
import requests

# ==================================================
# 🔧 設定區
# ==================================================
TELEGRAM_TOKEN = "8666112168:AAGaaRW0D5BTFgbItsMEhmeGzdkZhQnWvv8"
TELEGRAM_CHAT_ID = "997991682"
# ==================================================

def send_telegram(message):
    """發送訊息到 Telegram 手機"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": message}, timeout=5)
    except Exception as e:
        print(f"發送 Telegram 失敗: {e}")

def analyze_btc():
    """分析 BTC"""
    print(f"執行時間: {pd.Timestamp.now()}")

    try:
        exchange = ccxt.binance()
        ohlcv = exchange.fetch_ohlcv('BTC/USDT', timeframe='4h', limit=650)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        print(f"✅ 成功抓取 {len(df)} 根 K 線")
    except Exception as e:
        print(f"❌ 抓取數據失敗: {e}")
        return

    # 計算均線與 MACD
    for period in [36, 72, 144, 169, 288, 576]:
        df[f'ema_{period}'] = EMAIndicator(close=df['close'], window=period).ema_indicator()

    macd = MACD(close=df['close'])
    df['macd'] = macd.macd()
    df['signal'] = macd.macd_signal()
    df['histogram'] = macd.macd_diff()

    # 尋找 W底 和 M頂
    def find_pivot_lows(df, order=5):
        lows = df['low'].values
        return argrelextrema(lows, np.less, order=order)[0]

    def find_pivot_highs(df, order=5):
        highs = df['high'].values
        return argrelextrema(highs, np.greater, order=order)[0]

    recent_df = df.tail(40)
    pivot_lows = find_pivot_lows(recent_df, order=3)
    pivot_highs = find_pivot_highs(recent_df, order=3)

    # 檢查 W底
    w_pattern = False
    if len(pivot_lows) >= 2:
        idx1 = pivot_lows[-2]
        idx2 = pivot_lows[-1]
        if recent_df.iloc[idx2]['low'] > recent_df.iloc[idx1]['low']:
            ema144_val = recent_df.iloc[-1]['ema_144']
            low1_val = recent_df.iloc[idx1]['low']
            low2_val = recent_df.iloc[idx2]['low']
            if (abs(low1_val - ema144_val) / ema144_val < 0.10) or (abs(low2_val - ema144_val) / ema144_val < 0.10):
                w_pattern = True

    # 檢查 M頂
    m_pattern = False
    if len(pivot_highs) >= 2:
        idx1 = pivot_highs[-2]
        idx2 = pivot_highs[-1]
        if recent_df.iloc[idx2]['high'] < recent_df.iloc[idx1]['high']:
            ema144_val = recent_df.iloc[-1]['ema_144']
            high1_val = recent_df.iloc[idx1]['high']
            high2_val = recent_df.iloc[idx2]['high']
            if (abs(high1_val - ema144_val) / ema144_val < 0.10) or (abs(high2_val - ema144_val) / ema144_val < 0.10):
                m_pattern = True

    # 多空判斷
    latest = df.iloc[-1]
    ema_list = [36, 72, 144, 288, 576]
    trend_bullish = all(df[f'ema_{ema_list[i]}'].iloc[-1] > df[f'ema_{ema_list[i+1]}'].iloc[-1] for i in range(len(ema_list)-1))
    trend_bearish = all(df[f'ema_{ema_list[i]}'].iloc[-1] < df[f'ema_{ema_list[i+1]}'].iloc[-1] for i in range(len(ema_list)-1))
    above_576 = latest['close'] > latest['ema_576']
    macd_bullish = latest['macd'] > 0 and latest['histogram'] > 0
    macd_bearish = latest['macd'] < 0 and latest['histogram'] < 0

    print(f"價格: {latest['close']:.2f}, EMA144: {latest['ema_144']:.2f}, EMA576: {latest['ema_576']:.2f}")

    # 做多條件
    if above_576 and trend_bullish and macd_bullish and w_pattern:
        msg = f"🚀 BTC 做多訊號！\n價格: {latest['close']:.2f}\nEMA144: {latest['ema_144']:.2f}\nEMA576: {latest['ema_576']:.2f}\n時間: {latest['timestamp']}"
        print("✅ 強力做多信號！發送通知...")
        send_telegram(msg)
        return

    # 做空條件
    if not above_576 and trend_bearish and macd_bearish and m_pattern:
        msg = f"🚨 BTC 做空訊號！\n價格: {latest['close']:.2f}\nEMA144: {latest['ema_144']:.2f}\nEMA576: {latest['ema_576']:.2f}\n時間: {latest['timestamp']}"
        print("🔻 強力做空信號！發送通知...")
        send_telegram(msg)
        return

    print("📭 無強力信號")

if __name__ == "__main__":
    print("=" * 55)
    print("🤖 BTC 自動化策略（GitHub Actions 雲端版）")
    print("=" * 55)
    analyze_btc()
