"""
Represents a list of MarketDataQuotes
"""

from domain.market_data_quote import MarketDataQuote


class MarketDataStream:

    def __init__(self, quotes: list):
        # TODO:brandon.shute:2019-05-08: Add error handling
        self.__quotes = quotes
        self.__local_optima_indices

    def get_quotes(self) -> list:
        return self.__quotes

    def get_local_optima(self) -> list:
        if self.__local_optima_indices is None:
            self.__local_optima_indices = self.__get_local_optima_indices()
        return self.__local_optima_indices

    def __get_local_optima_indices(self) -> list:
        # The first and last index are always local optima
        indices = [0]
        for i in range(1, len(self.__quotes)):
            lower_quote = self.__quotes[i - 1]
            quote = self.__quotes[i]
            upper_quote = self.__quotes[i + 1]
            if self.__is_local_optima(lower_quote, quote, upper_quote):
                indices.append(i)
        indices.append(len(self.__quotes))
        return indices

    @staticmethod
    def __is_local_optima(lower_quote: MarketDataQuote, quote: MarketDataQuote, upper_quote: MarketDataQuote) -> bool:
        lower_value = lower_quote.get_rate()
        value = quote.get_rate()
        upper_value = upper_quote.get_rate()
        return (lower_value < value and upper_value < value) or \
                (lower_value >= value and upper_value >= value)
