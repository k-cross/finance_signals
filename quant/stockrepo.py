#!/usr/bin/python3
""" Stores and manages data for a specific ticker """

# from datetime import date
import bisect
from read_ticker_csv import get_stock_data


class repo(object):
    """
    Entire master repository of known history for a ticker. Useful for persisting data across multiple quantpredict runs.
    """

    def __init__(self, ticker):
        super(repo, self).__init__()
        self.ticker = ticker
        print("Get all history")
        self.history = []
        # self.orders = []

    # def load(self):
    #     """ Load previous processed results """
    #     with open(self.ticker + ".csv") as file:
    #         self.history = file.read()

    # def save(self):
    #     """ Save processed results """
    #     with open(self.ticker + ".csv") as file:
    #         # TODO: save as proper csv
    #         file.write(self.history)

    def populatehistory(self):
        """ Retrieve price history from csv """
        # Ordered old to new
        self.history = list(reversed(get_stock_data(self.ticker)))

    def locatedate(self, date):
        """ Find index of a requested day in historic data """
        a = [day['date'] for day in self.history]
        return bisect.bisect_left(a, date)

    def add_study(self, study_name, lst):
        """ Adds study data points to profile """
        for index, date in enumerate(self.history):
            date[study_name] = lst[index]

    def getplot(self, plot):
        """
        Get a particular series of data. Includes price and studies, not orders.
        For example, specify a study ('bb_lower'), or price ('c')
        """
        return [date[plot] for date in self.history]

    def getledger(self):
        """ Historic buy and sell orders """
        buy = []
        sell = []
        return buy, sell

    # def order(self, date, direction):
    #     """ logs an order at specified day """
    #     day = self.locatedate(date)
    #     self.history[day]['order'] = "buy"


class profile(object):
    """
    Information about a ticker with subset of entire history. Used to do operations and simulations on.
    """

    def __init__(self, ticker, history, repo=None):
        self.ticker = ticker
        self.history = history
        if repo is not None:
            if repo.ticker != self.ticker:
                raise Exception("Given repo with different ticker!")
            self.repo = repo

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

    def order(self, date, direction):
        """ logs an order at specified day """
        # Profile and repo history don't necessarily have same indexes
        today = len(self.history) - 1
        today = repo.locatedate(today)
        repo.history[today]['order'] = "buy"

    def getplot(self, plot):
        """
        Get a particular series of data.
        For example, specify a study ('bb_lower'), or price ('c')
        """
        return [date[plot] for date in self.history]
