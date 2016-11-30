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
# import csv

# Static Data
ticker = "AMZN"
csv = "../samples/%s.csv" % ticker
lines_5yr = 1260
history = []


def jumpTo(year, month, day):
    """ Find index of a requested day in historic data """
    d = datetime(year, month, day).date()
    return bisect.bisect_left([row[0] for row in history], d)


# Read history

# Consider using dictionary if it helps with quantpredict so you don't need indexes all the time or something
# https://docs.python.org/3/library/csv.html
line_counter = 0
with open(csv) as file:
    file.readline()  # remove csv header
    for line in file:
        line_counter += 1
        line = line.strip('\n')
        data = line.split(',')

        day = datetime.strptime(data[0], '%Y-%m-%d').date()
        # day = str(day)  # If date matters, remove str conversion
        op = round(float(data[1]), 2)
        hi = round(float(data[2]), 2)
        lo = round(float(data[3]), 2)
        cl = round(float(data[4]), 2)
        vol = int(data[5])

        history.insert(0, (day, op, hi, lo, cl, vol))

# Debug stuff
# print("read %i lines" % line_counter)
# for x in range(1, 10):
#     print(history[x])
# print(history[200])
# print(history[jumpTo(2011, 7, 1)])

# Analyze and make prediction

snapshot = copy.deepcopy(history[:jumpTo(2011, 7, 1)])

# Consider doing some OOP goodness with this:
# q = quantpredict(snapshot)
# q.analyze()
# q.predict()
# or something
quantpredict.analyze(snapshot)
