"""
Represents a rate for a currency pair
"""


class MarketDataQuote:

    def __init__(self, rate: float):
        self.__rate = rate

    def get_rate(self):
        return self.__rate
