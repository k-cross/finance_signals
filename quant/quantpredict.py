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
python list of historical stock price up until today

Out:
file/list with historical pricing and indicators/analysis
predicted future movement

Powered by magic and digital foxes
"""


import numpy as np
import talib.abstract as ta


class profile(object):
    """
    Information about a ticker, incl prices and studies
    """

    def __init__(self, ticker, pricing):
        self.ticker = ticker
        self.pricing = pricing  # Historic pricing and studies stored here

    # def load(self):
    #     """ Load previous processed results """
    #     with open(self.ticker + ".csv") as file:
    #         self.pricing = file.read()

    # def save(self):
    #     """ Save processed results """
    #     with open(self.ticker + ".csv") as file:
    #         # TODO: save as proper csv
    #         file.write(self.pricing)

    def addstudy(self, name, lst):
        """ Adds study data points to profile """
        for index, stkday in enumerate(self.pricing):
            stkday.ta[name] = lst[index]

    # def order(type):
    #     """ logs an order today """
    #     pass

    def getplot(self, plot):
        """
        Get a particular series of data.
        For example, specify a study ('bb_lower'), or price ('c')
        """
        return [stkday[plot] for stkday in self.pricing]


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
    prices = {'open': np.array([day.o for day in profile.pricing]),
              'high': np.array([day.h for day in profile.pricing]),
              'low': np.array([day.l for day in profile.pricing]),
              'close': np.array([day.c for day in profile.pricing]),
              'volume': np.array([day.vol for day in profile.pricing])}
    # print(prices['open'])
    # print(prices)

    sma = ta.SMA(prices, timeperiod=200)
    profile.addstudy("sma", [round(float(point), 2) for point in sma])

    bb_upper, bb_middle, bb_lower = ta.BBANDS(prices, 100, 2, 2)
    profile.addstudy("bb_upper", [round(float(point), 2) for point in bb_upper])
    profile.addstudy("bb_middle", [round(float(point), 2) for point in bb_middle])
    profile.addstudy("bb_lower", [round(float(point), 2) for point in bb_lower])

    rsi = ta.RSI(prices, timeperiod=14)
    profile.addstudy("rsi", [round(float(point), 2) for point in rsi])


def predict(profile):
    """
    Weighs different indicators from an analyzed profile, and deduce a prediction on future movement
    """
    today = len(profile.pricing) - 1
    stkday = profile.pricing[today]
    # print(todaysprice)
    # momentum = [stkday['bb_middle'], stkday['sma']]
    price = stkday.c

    if price > stkday.ta['bb_upper']:
        # print("Danger! Potential price correction, sell!")
        return -1
    elif price > stkday.ta['bb_middle'] and price > stkday.ta['sma']:
        # print("Figure out if it's in a channel")
        return 0
    elif price > stkday.ta['bb_lower'] and price < stkday.ta['sma']:
        # print("Down swing, avoid")
        return 0
    elif price < stkday.ta['bb_lower'] or price < stkday.ta['sma']:
        # print("Potentially undervalued, buy with caution")
        return 1
    else:
        return 0
