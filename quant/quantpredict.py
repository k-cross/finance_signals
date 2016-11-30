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


def analyze(history):
    """
    Documentation pending
    """
    # Placeholder print out first line of input
    print(history[0])
