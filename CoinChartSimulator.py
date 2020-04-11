import re
import random
import datetime
import pandas as pd

class CoinChartSimulator():
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

        #A list of each day's price change of the coin (from old to new).
        self.changes = []
        for i in range(len(self.prices) - 1):
            change = (self.prices[i + 1] - self.prices[i]) / self.prices[i]
            self.changes.append(change)

        #A price change list based on historical price, but made zero-sum.
        self.changes_z = []
        for i in self.changes:
            self.changes_z.append(i)
            self.changes_z.append(1 / (1 + i) - 1)

    def generate(self):
        """Generate a random price change (a double) from historical data."""
        return random.choice(self.changes)

    def generate_list(self, days=365):
        """Generate a list of random price changes (a list of doubles)."""
        return random.choices(self.changes, k=days)
    
    def simulate(self, start_price=0, days=365):
        """Generate a list of random price (a list of doubles)."""
        if start_price == 0:
            start_price = self.prices[-1]
        changes = self.generate_list(days=days)
        chart = [start_price]
        for i in range(days):
            chart.append(chart[i] * (1 + changes[i]))
        return chart

    #Below are the zero-sum versions of the methods above.
    def generate_z(self):
        """Generate a random (zero-sum) price change."""
        return random.choice(self.changes_z)

    def generate_list_z(self, days=365):
        """Generate a list of random (zero-sum) price changes."""
        return random.choices(self.changes_z, k=days)

    def simulate_z(self, start_price=0, days=365):
        """Generate a list of random (zero-sum) price."""
        if start_price == 0:
            start_price = self.prices[-1]
        changes = self.generate_list_z(days=days)
        chart = [start_price]
        for i in range(days):
            chart.append(chart[i] * (1 + changes[i]))
        return chart

btc = CoinChartSimulator('bitcoin')
print('Bitcoin prediction for the next 10 days...')
print(btc.simulate(start_price=btc.prices[-1], days=10))

doge = CoinChartSimulator('dogecoin')
print('Dogecoin prediction (zero-sum) for the next year...')
print(doge.simulate_z(start_price=doge.prices[-1], days=365))
