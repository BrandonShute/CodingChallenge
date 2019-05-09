"""
Represents a list of MarketDataQuotes
"""

from domain.market_data_quote import MarketDataQuote


class MarketDataStream:

    def __init__(self, quotes: list):
        # TODO:brandon.shute:2019-05-08: Add error handling
        self.__quotes = [MarketDataQuote(quote) for quote in quotes]
        self.__local_optima_flags = None

    def get_length(self) -> int:
        return len(self.__quotes)

    def get_quote(self, index: int) -> MarketDataQuote:
        return self.__quotes[index]

    def get_quotes(self) -> list:
        return self.__quotes

    def get_local_optima_flags(self) -> list:
        if self.__local_optima_flags is None:
            self.__local_optima_flags = [self.__is_local_optima(i) for i in range(len(self.__quotes))]
        return self.__local_optima_flags

    def __is_local_optima(self, index: int) -> bool:
        # The first and last index are always local optima
        if index == 0 or index == len(self.__quotes) - 1:
            return True

        lower_value = self.__quotes[index - 1].get_rate()
        value = self.__quotes[index].get_rate()
        upper_value = self.__quotes[index + 1].get_rate()
        return (lower_value < value and upper_value < value) or \
                (lower_value >= value and upper_value >= value)
