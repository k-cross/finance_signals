#!/usr/bin/python3
"""
Time Machine
Uses historical data to go back in time, and feeds quantpredict data that was available at that time. Use to compare with actual stock movement and check the performace of quantpredict.

In:
csv of ticker

Out:
historical prediction
accuracy of prediction
"""

from datetime import datetime
import quantpredict
import bisect
import copy
import matplotlib.pyplot as grapher
import sys
import statistics

# Static Data
ticker = 'AMZN'
samplespath = "../samples/%s.csv" % ticker
# lines_5yr = 1260
cumulativehistory = []


def locatedate(year, month, day):
    """ Find index of a requested day in historic data """
    d = datetime(year, month, day).date()
    return bisect.bisect_left([row['date'] for row in cumulativehistory], d)


def verifyprediction(stance, price, date, timeperiod=60, method='direction'):
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

    today = locatedate(date.year, date.month, date.day)
    window = cumulativehistory[today:today + timeperiod]
    score = 0
    print("stance %d, price %d, %s method" % (stance, price, method))

    if stance == 1:  # long
        # print("long stance")
        prices = [row['h'] for row in window]
        highest = max(prices)
        period_perc = (highest - price) / price
        period_median = (statistics.median(prices) - price) / price
    elif stance == -1:  # short
        # print("short stance")
        prices = [row['l'] for row in window]
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


# Read history

line_counter = 0
with open(samplespath) as file:
    file.readline()  # remove csv header
    for line in file:
        line_counter += 1
        line = line.strip('\n')
        data = line.split(',')
        # Insert entry and maintain ordering from old to new
        cumulativehistory.insert(0, {
            'date': datetime.strptime(data[0], '%Y-%m-%d').date(),
            'o': round(float(data[1]), 2),
            'h': round(float(data[2]), 2),
            'l': round(float(data[3]), 2),
            'c': round(float(data[4]), 2),
            'vol': int(data[5])})

# Debug stuff
# print("read %i lines" % line_counter)
# for x in range(0, 9):
#     print(cumulativehistory[x])
# print(cumulativehistory[200])
# print(cumulativehistory[locatedate(2011, 7, 1)])

# Analyze and make prediction

# Simulate today is july 1, 2011
start = locatedate(2011, 7, 1)  # ensure enough data for 200 SMA
end = line_counter

capital = 10000
profit = 0
holdings = 0

moves = 0
scores = []
scorelog = []

for x in range(start, end):
    # snapshot = copy.deepcopy(cumulativehistory[:locatedate(2012, 7, 1) + 1])
    snapshot = copy.deepcopy(cumulativehistory[:x + 1])
    q = quantpredict.profile(ticker, snapshot)
    quantpredict.analyze(q)
    stance = quantpredict.predict(q)
    if stance != 0:
        print("Outlook on day: " + str(x))
        moves += 1
    r = verifyprediction(stance, snapshot[x]['c'], snapshot[x]['date'], method="direction")
    if r is not None:
        round(r, 3)
        scores.append(r)
        scorelog.append((str(snapshot[x]['date']), r))

print("Avg performance of transactions: %f" % statistics.mean(scores))
print("Total moves: %d" % moves)
print("Total profitable moves: %d" % sum(x > 0 for x in scores))
print("Total high-performance moves: %d" % sum(x > 0.1 for x in scores))
print("Prediction accuracy: %f" % (sum(x > 0.05 for x in scores) / moves))
print("Full score log:")
for s in scorelog:
    print(s)
# print(profit)

# print("Outlook on day: " + str(cumulativehistory[start]['date']))
# # snapshot = copy.deepcopy(cumulativehistory[:locatedate(2012, 7, 1) + 1])
# snapshot = copy.deepcopy(cumulativehistory[:start + 1])
# # print(snapshot[len(snapshot) - 1])
# q = quantpredict.profile(ticker, snapshot)
# quantpredict.analyze(q)
# stance = quantpredict.predict(q)
# verifyprediction(stance, snapshot[start]['c'], snapshot[start]['date'], method="order")

# Sample plotting

if len(sys.argv) > 1:
    if sys.argv[1] == "--graph":
        # snapshot = copy.deepcopy(cumulativehistory)
        # q = quantpredict.profile(ticker, snapshot)
        # quantpredict.analyze(q)
        # quantpredict.predict(q)
        # print(q.priceplot())
        # grapher.subplot(211)
        grapher.plot(q.getplot('c'))
        grapher.plot(q.getplot('sma'))
        grapher.plot(q.getplot('bb_upper'))
        grapher.plot(q.getplot('bb_middle'))
        grapher.plot(q.getplot('bb_lower'))
        grapher.ylabel('price')

        # grapher.subplot(212)
        # grapher.plot(q.studies['rsi'])
        grapher.show()
    elif sys.argv[1] == "--graph-all":
        snapshot = copy.deepcopy(cumulativehistory)
        q = quantpredict.profile(ticker, snapshot)
        quantpredict.analyze(q)
        quantpredict.predict(q)
        # print(q.priceplot())
        # grapher.subplot(211)
        grapher.plot(q.getplot('c'))
        grapher.plot(q.getplot('sma'))
        grapher.plot(q.getplot('bb_upper'))
        grapher.plot(q.getplot('bb_middle'))
        grapher.plot(q.getplot('bb_lower'))
        grapher.ylabel('price')

        # grapher.subplot(212)
        # grapher.plot(q.studies['rsi'])
        grapher.show()
