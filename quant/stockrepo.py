#!/usr/bin/python3
"""
   _____ __             __   ____
  / ___// /_____  _____/ /__/ __ \___  ____  ____
  \__ \/ __/ __ \/ ___/ //_/ /_/ / _ \/ __ \/ __ \
 ___/ / /_/ /_/ / /__/ ,< / _, _/  __/ /_/ / /_/ /
/____/\__/\____/\___/_/|_/_/ |_|\___/ .___/\____/
                                   /_/
StockRepo

Stores and manages data for a specific ticker

Powered by magic and digital foxes
"""

import bisect
from read_ticker_csv import get_stock_data


class profile(object):
    """
    Information about a ticker with specified history subset. Includes prices and studies.
    """

    def __init__(self, ticker, history):
        self.ticker = ticker
        self.history = history  # Historic pricing and studies stored here

    # def load(self):
    #     """ Load previous processed results """
    #     with open(self.ticker + ".csv") as file:
    #         self.history = file.read()

    # def save(self):
    #     """ Save processed results """
    #     with open(self.ticker + ".csv") as file:
    #         # TODO: save as proper csv
    #         file.write(self.history)

    def add_study(self, study_name, lst):
        """ Adds study data points to profile """
        for index, date in enumerate(self.history):
            date[study_name] = lst[index]

    # def order(type):
    #     """ logs an order today """
    #     pass

    def getplot(self, plot):
        """
        Get a particular series of data.
        For example, specify a study ('bb_lower'), or price ('c')
        """
        return [date[plot] for date in self.history]


class repo(object):
    """
    Entire known history for a ticker. Useful for persisting data across multiple quantpredict runs.
    """

    def __init__(self, ticker):
        super(repo, self).__init__()
        self.ticker = ticker
        self.history = list(reversed(get_stock_data(ticker)))  # Ordered old to new
        self.orders = []

    def locatedate(self, date):
        """ Find index of a requested day in historic data """
        a = [day['date'] for day in self.history]
        return bisect.bisect_left(a, date)

    # def order(type):
    #     """ logs an order today """
    #     pass
