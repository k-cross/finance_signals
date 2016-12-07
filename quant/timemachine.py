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
import copy
import matplotlib.pyplot as grapher
import sys
import statistics
import argparse

import quantpredict
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


def historytrials():
    pass


def stockgraph(repo, studies=False, orders=False):
    if studies and "rsi" in args.studies:
        grapher.subplot(211)
    grapher.plot(repo.getplot('c'))
    grapher.ylabel('price')
    if studies:
        if "sma" in args.studies:
            grapher.plot(repo.getplot('sma'))
        if "bb" in args.studies:
            grapher.plot(repo.getplot('bb_upper'))
            grapher.plot(repo.getplot('bb_middle'))
            grapher.plot(repo.getplot('bb_lower'))
        if "rsi" in args.studies:
            grapher.subplot(212)
            grapher.plot(repo.getplot('rsi'))
    if orders:
        grapher.plot(repo.getplot('order'))
    grapher.show()


parser = argparse.ArgumentParser(description='Time machine to go back in time and test trading algorithm on historical data.')
# parser.add_argument('integers', metavar='N', type=int, nargs='+', help='an integer for the accumulator')
parser.add_argument('ticker', help='stock ticker being examined')

# General args
parser.add_argument('--from', dest='from', help='starting point of time machine')
parser.add_argument('--to', dest='to', help='ending point of time machine')

# Graphing args
group = parser.add_mutually_exclusive_group()
group.add_argument('--graph', dest='graph', action='store_true', help='graph a portion of the stock history')
group.add_argument('--graph-all', dest='graphall', action='store_true', help='graph entire stock repo')
parser.add_argument('--studies', dest='studies', nargs='+', help='studies to draw on the graph (SMA, BB, RSI)')
parser.add_argument('--orders', dest='orders', action='store_true', help='draw orders on stock graph')
args = parser.parse_args()

# Read history

ticker = args.ticker
if len(sys.argv) > 1:
    ticker = args.ticker
else:
    sys.exit("No ticker!")
repo = stockrepo.repo(ticker)

# Analyze and make prediction

quantpredict.analyze(repo)

# Simulate today is july 1, 2011

start = repo.locatedate(date(2011, 7, 1))  # ensure enough data for 200 SMA
end = len(repo.history)

moves = 0
scores = []
scorelog = []

for x in range(start, end):
    # snapshot = copy.deepcopy(repo.history[:repo.locatedate(2012, 7, 1) + 1])
    # snapshot = copy.deepcopy(repo.history[:x + 1])
    # p, stance = qppredict(snapshot)
    tradingday = repo.history[x]
    stance = quantpredict.predict(repo, tradingday['date'])
    if stance != 0:
        print("Outlook on %s, day %d" % (tradingday['date'], x))
        moves += 1
        r = verifyprediction(stance, tradingday['c'], tradingday['date'], method="direction")
    # if r is not None:
        round(r, 3)
        scores.append(r)
        scorelog.append((str(tradingday['date']), r))

print("Avg performance of transactions: %f" % statistics.mean(scores))
print("Total moves: %d" % moves)
print("Total profitable moves: %d" % sum(x > 0 for x in scores))
print("Total high-performance moves: %d" % sum(x > 0.1 for x in scores))
print("Prediction accuracy: %f" % (sum(x > 0.05 for x in scores) / moves))
print("Full score log:")
for s in scorelog:
    print(s)
# print(profit)

# print("Outlook on day: " + str(repo.history[start]['date']))
# # snapshot = copy.deepcopy(repo.history[:repo.locatedate(2012, 7, 1) + 1])
# snapshot = copy.deepcopy(repo.history)
# # print(snapshot[len(snapshot) - 1])
# p, stance = qppredict(snapshot)
# verifyprediction(stance, snapshot[start]['c'], snapshot[start]['date'], method="order")

# Sample plotting

if args.graph:
    stockgraph(repo, studies=args.studies, orders=args.orders)
    # Currently no difference
elif args.graphall:
    stockgraph(repo, studies=args.studies, orders=args.orders)
