import re
import datetime
import random
import pandas as pd

def choose_coin():
    """Let user choose a coin, return coin name."""
    print('Top 20 cryptocurrencies:\n')
    url = 'https://coinmarketcap.com/'
    df = pd.read_html(url)[2]
    df.style.hide_index()
    print(df.loc[0:19, ['#', 'Name', 'Market Cap', 'Price', 'Change (24h)']]
          .to_string(index = False))
    num = int(input('\nType the # you want: ')) - 1
    coin_name = df['Name'][num]
    print(f'\nYou chose {coin_name}.')
    return coin_name

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
        self.zero_sum_list = []
        for i in self.changes:
            self.zero_sum_list.append(abs(i))
            self.zero_sum_list.append(1 / (1 + abs(i)) - 1)
            self.zero_sum_list.append(-abs(i))
            self.zero_sum_list.append(1 / (1 - abs(i)) - 1)

    def generate(self):
        """Generate a random price change (a double) from historical data."""
        return random.choice(self.changes)

    def generate_list(self, days=365):
        """Generate a list of random price changes (a list of doubles)."""
        return random.choices(self.changes, k=days)
    
    def simulate(self, start_price=100, days=365):
        """Generate a list of random price (a list of doubles)."""
        changes = self.generate_list(days=days)
        chart = [start_price]
        for i in range(days):
            chart.append(chart[i] * (1 + changes[i]))
        return chart

    #Below are the zero-sum versions of the methods above.
    def generate_z(self):
        """Generate a random (zero-sum) price change."""
        return random.choice(self.zero_sum_list)

    def generate_list_z(self, days=365):
        """Generate a list of random (zero-sum) price changes."""
        return random.choices(self.zero_sum_list, k=days)

    def simulate_z(self, start_price=100, days=365):
        """Generate a list of random (zero-sum) price."""
        changes = self.generate_list_z(days=days)
        chart = [start_price]
        for i in range(days):
            chart.append(chart[i] * (1 + changes[i]))
        return chart

btc = CoinChartSimulator('bitcoin')
print(btc.simulate_z(start_price=btc.prices[-1], days=365))
