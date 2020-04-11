# CoinChartSimulator

The aim is to generate random data to do simulations to test investment strategies.
This is based on the assumption that cryptocurrency price fluctuations are random.
Another assumption, that cryptocurrency markets are zero-sum, is also featured.

We use historical cryptocurrency price as a selection pool to randomly sample from.
Simulations generated from which will preserve the coin value's volatility.
However, the expected value of the coin value will also linger, which may seem too optimistic for some coins and pessimistic for others.
Therefore we added mirrored price change data into the selection pool to make the generator zero-summed, meaning that after any given period of time the coin price will always have 50% chance to have gone up and 50% chance to have gone down.
