#!/usr/bin/python3
"""
   ____                    __  ____                ___      __
  / __ \__  ______ _____  / /_/ __ \________  ____/ (_)____/ /_
 / / / / / / / __ `/ __ \/ __/ /_/ / ___/ _ \/ __  / / ___/ __/
/ /_/ / /_/ / /_/ / / / / /_/ ____/ /  /  __/ /_/ / / /__/ /_
\___\_\__,_/\__,_/_/ /_/\__/_/   /_/   \___/\__,_/_/\___/\__/
QuantPredict

Given data for a stock's historical movement, uses quantitative analysis, technical analysis, and other indicators to predict the future movement of a stock.

Currently calibrated to daily movement; intraday not supported.

'Studies' is synonymous with 'technical indicators'.

In:
profile or repo from stockrepo

Out:
file/list with historical pricing and indicators/analysis
predicted future movement

Powered by magic and digital foxes
"""

import numpy as np
import talib.abstract as ta


def analyze(profile):
    """
    Compute studies and draw conclusions about stock's performance

    Development note: hard cutoffs (T/F) are discouraged, instead use arithmetic operations, percentages, etc.

    In: profile with basic ohlc price data
    Out: updated with studies and analysis about historic performance
    """
    # Update profile with technical indicators
    technical(profile)
    # Parse and draw conclusions from technical data


def technical(profile):
    """
    Updates profile with SMA, BB, and RSI calculations

    In: profile with basic ohlc price data
    Out: profile updated with studies merged with profile's price history
    """
    prices = {'open': np.array([record['o'] for record in profile.history]),
              'high': np.array([record['h'] for record in profile.history]),
              'low': np.array([record['l'] for record in profile.history]),
              'close': np.array([record['c'] for record in profile.history]),
              'volume': np.array([record['vol'] for record in profile.history])}
    # print(prices['open'])
    # print(prices)

    sma = ta.SMA(prices, timeperiod=200)
    profile.add_study("sma", [round(float(point), 2) for point in sma])

    bb_upper, bb_middle, bb_lower = ta.BBANDS(prices, 100, 2, 2)
    profile.add_study("bb_upper", [round(float(point), 2) for point in bb_upper])
    profile.add_study("bb_middle", [round(float(point), 2) for point in bb_middle])
    profile.add_study("bb_lower", [round(float(point), 2) for point in bb_lower])

    rsi = ta.RSI(prices, timeperiod=14)
    profile.add_study("rsi", [round(float(point), 2) for point in rsi])


def predict(profile):
    """
    Weighs different indicators from an analyzed profile, and deduce a prediction on future movement
    """
    today = len(profile.history) - 1
    today = profile.history[today]
    # print(todaysprice)
    # momentum = [today['bb_middle'], today['sma']]
    price = today['c']

    if price > today['bb_upper']:
        # print("Danger! Potential price correction, sell!")
        return -1
    elif price > today['bb_middle'] and price > today['sma']:
        # print("Figure out if it's in a channel")
        return 0
    elif price > today['bb_lower'] and price < today['sma']:
        # print("Down swing, avoid")
        return 0
    elif price < today['bb_lower'] or price < today['sma']:
        # print("Potentially undervalued, buy with caution")
        return 1
    else:
        return 0
