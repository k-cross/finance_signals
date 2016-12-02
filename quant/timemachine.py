#!/usr/bin/python3
"""
  _______                __  ___           __    _
 /_  __(_)___ ___  ___  /  |/  /___ ______/ /_  (_)___  ___
  / / / / __ `__ \/ _ \/ /|_/ / __ `/ ___/ __ \/ / __ \/ _ \
 / / / / / / / / /  __/ /  / / /_/ / /__/ / / / / / / /  __/
/_/ /_/_/ /_/ /_/\___/_/  /_/\__,_/\___/_/ /_/_/_/ /_/\___/
Time Machine

General purpose tool for interfacing with quantpredict. Reads stock data from csv.

Usage (coming soon):

timemachine.py --ticker <ticker> ...

    predict <date>
        Generate prediction for a specified date

    historic [--from <date> --to <date>]
        Uses historical data to go back in time, and feeds quantpredict data that was available at that time. Compares the result with actual stock movement to determine performace of quantpredict. Prints out the results.

    graph [all | --from <date> --to <date>] [--studies [SMA | BB | RSI]]
        Draws graph with technical analysis overlaid. Entire graph shown by default.

Powered by magic and digital foxes
"""

from datetime import date
import quantpredict
import copy
import matplotlib.pyplot as grapher
import sys
import statistics

import stockrepo


def qppredict(snapshot):
    """ Executes quantpredict analysis on a given price snapshot """
    p = stockrepo.profile(ticker, snapshot)
    quantpredict.analyze(p)
    stance = quantpredict.predict(p)
    return p, stance


def verifyprediction(stance, price, decisiondate, timeperiod=60, method='direction'):
    """
    Determine if the predicted stance is correct.

    If method is direction, prediction for general direction is checked. The median closing price of the following days within the timeperiod limit is compared to the price passed in.

    If method is order, prediction is treated as actual order and expected to be profitable within the timeperiod. Price needs to move at least 5% in the desired direction. Return is how much more or less than percentage target the ticker reached in highest/lowest intraday trading.

    i.e. a buy order at 100 would look for a high of 105 in the next X (timeperiod) days. A sell order at 100 looks for a low of 95 or less before declaring success.

    In:
    details of the prediction
    stance of prediction as 1 or -1, long or short, buy or sell
    closing price of that day
    date prediction made on

    Out:
    a number representing percentage movement relative to horizon. Positive is desireable, negative means price movement in opposite to prediction.
    """
    if stance == 0:
        # print("hold steady")
        return

    today = repo.locatedate(decisiondate)
    window = repo.history[today:today + timeperiod]
    score = 0
    print("stance %d, price %d, %s method" % (stance, price, method))

    if stance == 1:  # long
        # print("long stance")
        prices = [day['h'] for day in window]
        highest = max(prices)
        period_perc = (highest - price) / price
        period_median = (statistics.median(prices) - price) / price
    elif stance == -1:  # short
        # print("short stance")
        prices = [day['l'] for day in window]
        lowest = min(prices)
        period_perc = (price - lowest) / price
        period_median = (price - statistics.median(prices)) / price

    # print(', '.join([str(p) for p in prices]))
    # print(list(map(check, prices)))
    # print(min(prices))
    # print(statistics.median(prices))

    if stance != 0:
        if method == 'direction':
            # Percentage difference with actual performance's median over timeperiod
            score = period_median
        elif method == 'order':
            # Note this method is broken
            score = period_perc
        print("score: " + str(score))
        return score
    else:
        return None


def stockgraph(repo, studies=False, orders=False):
    p, stance = qppredict(repo.history)
    # grapher.subplot(211)
    grapher.plot(p.getplot('c'))
    grapher.ylabel('price')
    if studies:
        grapher.plot(p.getplot('sma'))
        grapher.plot(p.getplot('bb_upper'))
        grapher.plot(p.getplot('bb_middle'))
        grapher.plot(p.getplot('bb_lower'))
    if orders:
        grapher.plot(p.getplot)
    # grapher.subplot(212)
    # grapher.plot(p.studies['rsi'])
    grapher.show()

# Read history

ticker = ""
if len(sys.argv) > 1:
    ticker = sys.argv[1]
else:
    sys.exit("No ticker!")
repo = stockrepo.repo(ticker)

# Analyze and make prediction

quantpredict.analyze(repo)
quantpredict.

# Simulate today is july 1, 2011
# start = repo.locatedate(date(2011, 7, 1))  # ensure enough data for 200 SMA
# end = len(repo.history)

# moves = 0
# scores = []
# scorelog = []

# for x in range(start, end):
#     # snapshot = copy.deepcopy(repo.history[:repo.locatedate(2012, 7, 1) + 1])
#     snapshot = copy.deepcopy(repo.history[:x + 1])
#     p, stance = qppredict(snapshot)
#     if stance != 0:
#         print("Outlook on day: " + str(x))
#         moves += 1
#     r = verifyprediction(stance, snapshot[x]['c'], snapshot[x]['date'], method="direction")
#     if r is not None:
#         round(r, 3)
#         scores.append(r)
#         scorelog.append((str(snapshot[x]['date']), r))

# print("Avg performance of transactions: %f" % statistics.mean(scores))
# print("Total moves: %d" % moves)
# print("Total profitable moves: %d" % sum(x > 0 for x in scores))
# print("Total high-performance moves: %d" % sum(x > 0.1 for x in scores))
# print("Prediction accuracy: %f" % (sum(x > 0.05 for x in scores) / moves))
# print("Full score log:")
# for s in scorelog:
#     print(s)
# print(profit)

# print("Outlook on day: " + str(repo.history[start]['date']))
# # snapshot = copy.deepcopy(repo.history[:repo.locatedate(2012, 7, 1) + 1])
# snapshot = copy.deepcopy(repo.history)
# # print(snapshot[len(snapshot) - 1])
# p, stance = qppredict(snapshot)
# verifyprediction(stance, snapshot[start]['c'], snapshot[start]['date'], method="order")

# Sample plotting

if len(sys.argv) > 2:
    if sys.argv[2] == "--graph":
        p, stance = qppredict(repo.history)
        # grapher.subplot(211)
        grapher.plot(p.getplot('c'))
        grapher.plot(p.getplot('sma'))
        grapher.plot(p.getplot('bb_upper'))
        grapher.plot(p.getplot('bb_middle'))
        grapher.plot(p.getplot('bb_lower'))
        grapher.ylabel('price')

        # grapher.subplot(212)
        # grapher.plot(p.studies['rsi'])
        grapher.show()
    elif sys.argv[2] == "--graph-all":
        p, stance = qppredict(repo.history)
        quantpredict.analyze(p)
        quantpredict.predict(p)
        # print(p.priceplot())
        # grapher.subplot(211)
        grapher.plot(p.getplot('c'))
        grapher.plot(p.getplot('sma'))
        grapher.plot(p.getplot('bb_upper'))
        grapher.plot(p.getplot('bb_middle'))
        grapher.plot(p.getplot('bb_lower'))
        grapher.ylabel('price')

        # grapher.subplot(212)
        # grapher.plot(p.studies['rsi'])
        grapher.show()
