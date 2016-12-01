#!/usr/bin/python3
"""
   ____                    __  ____                ___      __
  / __ \__  ______ _____  / /_/ __ \________  ____/ (_)____/ /_
 / / / / / / / __ `/ __ \/ __/ /_/ / ___/ _ \/ __  / / ___/ __/
/ /_/ / /_/ / /_/ / / / / /_/ ____/ /  /  __/ /_/ / / /__/ /_
\___\_\__,_/\__,_/_/ /_/\__/_/   /_/   \___/\__,_/_/\___/\__/
QuantPredict

Given some data for a stock's historical movement, uses quantitative analysis, technical analysis, and other indicators to predict the future movement of a stock.

Currently calibrated to daily movement; intraday not supported.

In:
python list of historical stock price up until today

Out:
file/list with historical pricing and indicators/analysis
predicted future movement

Powered by magic and digital foxes
"""

import numpy as np
import talib.abstract as ta
# import talib.abstract as tech


# sma = abstract.SMA
# bband = abstract.BBANDS
# rsi = abstract.RSI


class profile(object):
    """
    General info about a ticker. 'Studies' is synonymous with 'technical indicators'.
    """

    def __init__(self, ticker, pricing):
        self.ticker = ticker
        self.pricing = pricing
        # self.studies = {}

    def load(self):
        """ Load previous processed results """
        with open(self.ticker + ".csv") as file:
            self.pricing = file.read()

    def save(self):
        """ Save processed results """
        with open(self.ticker + ".csv") as file:
            # TODO: save as proper csv
            file.write(self.pricing)

    def add_study(self, study_name, lst):
        """ Adds study data points to profile """
        # self.studies[study_name] = lst
        # print(len(self.pricing))
        # print(len(lst))
        for index, date in enumerate(self.pricing):
            date[study_name] = lst[index]

    def getplot(self, plot):
        return [date[plot] for date in self.pricing]


def analyze(profile):
    """
    Compute studies and draw conclusions about stock's performance
    """
    # Update profile with technical indicators
    technical(profile)
    # Parse and draw conclusions from technical data


def technical(profile):
    """
    Updates profile with SMA, BB, and RSI calculations
    In: profile with relevant data
    """
    prices = {'open': np.array([record['o'] for record in profile.pricing]),
              'high': np.array([record['h'] for record in profile.pricing]),
              'low': np.array([record['l'] for record in profile.pricing]),
              'close': np.array([record['c'] for record in profile.pricing]),
              'volume': np.array([record['vol'] for record in profile.pricing])}
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
    today = len(profile.pricing) - 1
    data = profile.pricing[today]
    # print(todaysprice)
    # momentum = [data['bb_middle'], data['sma']]
    if data['c'] > data['bb_middle'] and data['c'] > data['sma']:
        print("Strong!")
    else:
        print("Don't buy!")
