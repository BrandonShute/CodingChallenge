"""
Represents the current market environment (rates, fees, etc.)
"""

import pandas as pd


class MarketEnvironment:

    def __init__(self, quotes_streams: dict, fees: dict):
        self.__quotes_streams = quotes_streams
        self.__fees = fees

    def get_trading_decision_points(self) -> list:
        all_local_optima = [quotes.get_local_optima() for quotes in self.__quotes_streams]
        # Remove duplicates
        return list(dict.fromkeys(all_local_optima))

    def get_profit_and_loss_for_all(self, investment: float, buy_index: int, sell_index: int) -> dict:
        profit_and_loss = {}
        for instrument in self.__quotes_streams.keys():
            profit_and_loss[instrument] = self.get_profit_and_loss(investment, buy_index, sell_index, instrument)
        return profit_and_loss

    def get_profit_and_loss(self, investment: float, buy_index: int, sell_index: int, instrument: str) -> float:
        # TODO:brandon.shute:2019-05-08: Error handle indices and instrument
        return investment * (self.__quotes_streams[instrument][sell_index] - self.__quotes_streams[instrument][buy_index]) - self.__fees[instrument]

    def get_fee(self, instrument: str) -> float:
        # TODO:brandon.shute:2019-05-08: Error handle indices and instrument
        return self.__fees[instrument]

    @staticmethod
    def from_csv(market_data_location: str, fee_location: str):
        market_data_df = pd.read_csv(market_data_location)
        fee_data_df = pd.read_csv(fee_location)
        return MarketEnvironment(market_data_df.to_dict(), fee_data_df.to_dict())
