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
# import _tkinter
# import csv

# Static Data
ticker = "AMZN"
samplespath = "../samples/%s.csv" % ticker
lines_5yr = 1260
cumulativehistory = []


def jumpTo(year, month, day):
    """ Find index of a requested day in historic data """
    d = datetime(year, month, day).date()
    return bisect.bisect_left([row['date'] for row in cumulativehistory], d)


# Read history

# Consider using dictionary if it helps with quantpredict so you don't need indexes all the time or something
# https://docs.python.org/3/library/csv.html
line_counter = 0
with open(samplespath) as file:
    file.readline()  # remove csv header
    for line in file:
        line_counter += 1
        line = line.strip('\n')
        data = line.split(',')
        d = {'date': datetime.strptime(data[0], '%Y-%m-%d').date(),
             'o': round(float(data[1]), 2),
             'h': round(float(data[2]), 2),
             'l': round(float(data[3]), 2),
             'c': round(float(data[4]), 2),
             'vol': int(data[5])}
        cumulativehistory.insert(0, d)

# Debug stuff
# print("read %i lines" % line_counter)
# for x in range(0, 9):
#     print(cumulativehistory[x])
# print(cumulativehistory[200])
# print(cumulativehistory[jumpTo(2011, 7, 1)])

# Analyze and make prediction

# Simulate today is july 1, 2011
snapshot = copy.deepcopy(cumulativehistory[:jumpTo(2012, 7, 1) + 1])
q = quantpredict.profile(ticker, snapshot)
quantpredict.analyze(q)
quantpredict.predict(q)

# Sample plotting

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
