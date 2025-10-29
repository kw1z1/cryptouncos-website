# main/services.py
import requests
import json
import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

class CryptoService:
    @staticmethod
    def get_crypto_prices():
        try:
            url = "https://api.coingecko.com/api/v3/simple/price"
            params = {
                'ids': 'bitcoin,ethereum,cardano',
                'vs_currencies': 'usd',
                'include_24hr_change': 'true'
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            crypto_data = [
                {
                    'symbol': 'BTC',
                    'name': 'Bitcoin',
                    'icon': '₿',
                    'price': data['bitcoin']['usd'],
                    'change': data['bitcoin']['usd_24h_change']
                },
                {
                    'symbol': 'ETH', 
                    'name': 'Ethereum',
                    'icon': 'Ξ',
                    'price': data['ethereum']['usd'],
                    'change': data['ethereum']['usd_24h_change']
                },
                {
                    'symbol': 'ADA',
                    'name': 'Cardano', 
                    'icon': '₳',
                    'price': data['cardano']['usd'],
                    'change': data['cardano']['usd_24h_change']
                }
            ]
            
            return crypto_data
            
        except Exception as e:
            return [
                {'symbol': 'BTC', 'name': 'Bitcoin', 'icon': '₿', 'price': 42158.76, 'change': 2.3},
                {'symbol': 'ETH', 'name': 'Ethereum', 'icon': 'Ξ', 'price': 2845.32, 'change': 1.8},
                {'symbol': 'ADA', 'name': 'Cardano', 'icon': '₳', 'price': 0.4521, 'change': -0.5}
            ]

    @staticmethod
    def get_bitcoin_chart_data(days=30):
        """Генерируем реалистичные данные для японских свечей"""
        try:
            # Получаем реальные данные от CoinGecko
            url = f"https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
            params = {
                'vs_currency': 'usd',
                'days': days,
                'interval': 'hourly' if days <= 7 else 'daily'
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            prices = data['prices']
            ohlc_data = []
            
            # Конвертируем в OHLC формат (Open, High, Low, Close)
            for i in range(0, len(prices), 24 if days > 7 else 6):  # Группируем по дням/часам
                chunk = prices[i:i+24] if days > 7 else prices[i:i+6]
                if len(chunk) > 0:
                    opens = [p[1] for p in chunk]
                    timestamp = chunk[0][0]
                    ohlc_data.append({
                        'timestamp': timestamp,
                        'open': opens[0],
                        'high': max(opens),
                        'low': min(opens),
                        'close': opens[-1],
                        'volume': random.uniform(1000000, 50000000)
                    })
            
            return ohlc_data[-100:]  # Возвращаем последние 100 точек
            
        except Exception as e:
            # Fallback - генерируем реалистичные данные
            return CryptoService.generate_fallback_chart_data(days)

    @staticmethod
    def generate_fallback_chart_data(days):
        """Генерация реалистичных данных свечей"""
        base_price = 40000
        data = []
        current_time = datetime.now()
        
        for i in range(100):
            timestamp = current_time - timedelta(hours=(99-i)*24)
            
            # Реалистичные движения цены
            volatility = 0.02  # 2% волатильность
            change = np.random.normal(0, volatility)
            
            if i == 0:
                open_price = base_price
            else:
                open_price = data[i-1]['close']
            
            close_price = open_price * (1 + change)
            high_price = max(open_price, close_price) * (1 + abs(np.random.normal(0, 0.01)))
            low_price = min(open_price, close_price) * (1 - abs(np.random.normal(0, 0.01)))
            
            data.append({
                'timestamp': int(timestamp.timestamp() * 1000),
                'open': open_price,
                'high': high_price,
                'low': low_price,
                'close': close_price,
                'volume': random.uniform(1000000, 50000000)
            })
        
        return data

    @staticmethod
    def calculate_indicators(ohlc_data):
        """Рассчитываем технические индикаторы"""
        if not ohlc_data:
            return {}
            
        closes = [candle['close'] for candle in ohlc_data]
        
        # SMA (Simple Moving Average)
        sma_20 = sum(closes[-20:]) / min(20, len(closes))
        sma_50 = sum(closes[-50:]) / min(50, len(closes))
        
        # RSI (Relative Strength Index)
        rsi = CryptoService.calculate_rsi(closes)
        
        # MACD
        macd, signal = CryptoService.calculate_macd(closes)
        
        # Прогноз на основе индикаторов
        prediction = CryptoService.generate_prediction(closes, sma_20, sma_50, rsi, macd)
        
        return {
            'sma_20': sma_20,
            'sma_50': sma_50,
            'rsi': rsi,
            'macd': macd,
            'signal': signal,
            'prediction': prediction
        }

    @staticmethod
    def calculate_rsi(prices, period=14):
        if len(prices) < period + 1:
            return 50
            
        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])
        
        if avg_loss == 0:
            return 100
            
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return round(rsi, 2)

    @staticmethod
    def calculate_macd(prices, fast=12, slow=26, signal=9):
        if len(prices) < slow:
            return 0, 0
            
        ema_fast = CryptoService.ema(prices, fast)
        ema_slow = CryptoService.ema(prices, slow)
        macd_line = ema_fast - ema_slow
        signal_line = CryptoService.ema([macd_line], signal)
        
        return round(macd_line, 2), round(signal_line, 2)

    @staticmethod
    def ema(prices, period):
        if len(prices) < period:
            return prices[-1] if prices else 0
            
        multiplier = 2 / (period + 1)
        ema_value = prices[0]
        
        for price in prices[1:]:
            ema_value = (price - ema_value) * multiplier + ema_value
            
        return ema_value

    @staticmethod
    def generate_prediction(closes, sma_20, sma_50, rsi, macd):
        """Генерируем AI прогноз на основе индикаторов"""
        current_price = closes[-1] if closes else 40000
        
        # Простая логика прогноза
        if sma_20 > sma_50 and rsi < 70 and macd > 0:
            direction = "BULLISH"
            confidence = random.randint(65, 85)
            target_low = current_price * 1.02
            target_high = current_price * 1.08
        elif sma_20 < sma_50 and rsi > 30 and macd < 0:
            direction = "BEARISH" 
            confidence = random.randint(60, 80)
            target_low = current_price * 0.92
            target_high = current_price * 0.98
        else:
            direction = "NEUTRAL"
            confidence = random.randint(40, 60)
            target_low = current_price * 0.98
            target_high = current_price * 1.02
        
        return {
            'direction': direction,
            'confidence': confidence,
            'target_low': round(target_low, 2),
            'target_high': round(target_high, 2),
            'current_price': round(current_price, 2)
        }