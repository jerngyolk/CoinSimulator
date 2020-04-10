import re
import datetime
import random
import pandas as pd

class Generator():
    """Generate random price changes for simulations."""
    def __init__(self, coin_name):
        url = 'https://coinmarketcap.com/currencies/' + \
              re.sub(r'[\W]', '-', coin_name) + \
              '/historical-data/?start=20130429&end=' + \
              str(datetime.date.today()).replace('-', '')
        #Pandas dataframe of the coin historical data from CMC.
        self.df = pd.read_html(url)[2]

        #A list of each day's close price of the coin (from old to new).
        self.prices = list(reversed(self.df['Close**'].tolist()))

        #A list of each day's price-change of the coin (from old to new).
        self.changes = []
        for i in range(len(self.prices) - 1):
            change = (self.prices[i + 1] - self.prices[i]) / self.prices[i]
            self.changes.append(change)

        #A price change list based on historical price, but made zero-sum.
        self.zero_sum_list = []
        for i in self.changes:
            self.zero_sum_list.append(abs(i))
            self.zero_sum_list.append(1 / (1 + abs(i)) - 1)
            self.zero_sum_list.append(-abs(i))
            self.zero_sum_list.append(1 / (1 - abs(i)) - 1)

    def change(self):
        """Generate a random price change from historical data."""
        return random.choice(self.changes)

    def changes(self, days=1):
        """Generate a list of random price changes."""
        return random.choices(self.changes, k=days)

    def zero_summed_change(self):
        """Generate a random price change (zero-sum)."""
        return random.choice(self.zero_sum_list)

    def zero_summed_changes(self, days=1):
        """Generate a list of random price changes (zero-sum)."""
        return random.choices(self.zero_sum_list, k=days)
