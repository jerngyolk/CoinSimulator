import re
import random
import datetime
import pandas as pd

class CoinSimulator():
    """Generate random prices for simulations."""
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


class Tester():
    """Take in a list of coin prices to test investment performance."""
    def __init__(self, price_list):
        self.price_list = price_list
        self.money_spent = 0
        self.money_in = 0
        self.coins_owned = 0
        self.coins_value = 0

    def buy(self, price, usd=0, coins=0, imprint=False):
        """Buy coins, need price and amount (usd or coin)."""
        spent = usd + coins * price
        self.money_spent += spent
        self.money_in += spent
        self.coins_owned += spent / price
        if imprint:
            print(f'\nSpent ${spent} buying {spent / price} coins.')
            print(f'Total spent: ${self.money_spent}')
            print(f'Money in: ${self.money_in}')
            print(f'Coins owned: {self.coins_owned}')
            

    def sell(self, price, usd=0, coins=0, imprint=False):
        """Sell coins, need price and amount (usd or coin)."""
        received = usd + coins * price
        self.money_in -= received
        self.coins_owned -= received / price
        if imprint:
            print(f'\nReceived ${received} selling {received / price} coins.')
            print(f'Total spent: ${self.money_spent}')
            print(f'Money in: ${self.money_in}')
            print(f'Coins owned: {self.coins_owned}')
            

    def performance(self, imprint=False):
        """Calculate investment return."""
        self.coins_value = round(self.coins_owned * self.price_list[-1], 2)
        solled = round(self.money_spent - self.money_in, 2)
        total_value = round(self.coins_value + solled, 2)
        performance = (total_value - self.money_spent) / self.money_spent
        if imprint:
            print('\nPerformance:')
            print(f'Coin value: ${self.coins_value}')
            print(f'Value of coins already sold: ${solled}')
            print(f'Total value: ${total_value}')
            print(f'Total spent: ${round(self.money_spent, 2)}')
            print(f'Return: {round(performance * 100, 2)}%')
        return performance


btc = CoinSimulator('bitcoin')
btc_list = btc.simulate(start_price=btc.prices[-1], days=1000)
#btc_list = btc.prices

print('Simulated btc periodic investment:')

print('\nEvery day:')
every_day = Tester(btc_list)
for i in range(len(btc_list)):
    every_day.buy(price=btc_list[i], usd=1000)
every_day.performance(imprint=True)

print('\nEvery week:')
every_week = Tester(btc_list)
for i in range(len(btc_list)):
    if i % 7 == 0:
        every_week.buy(price=btc_list[i], usd=1000)
every_week.performance(imprint=True)

print('\nEvery month:')
every_month = Tester(btc_list)
for i in range(len(btc_list)):
    if i % 30 == 0:
        every_month.buy(price=btc_list[i], usd=1000)
every_month.performance(imprint=True)

print('\nEvery 6 months:')
every_six_months = Tester(btc_list)
for i in range(len(btc_list)):
    if i % 183 == 0:
        every_six_months.buy(price=btc_list[i], usd=1000)
every_six_months.performance(imprint=True)
