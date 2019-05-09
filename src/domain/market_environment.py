"""
Represents the current market environment (rates, fees, etc.)
"""

import pandas as pd
from domain.market_data_stream import MarketDataStream


class MarketEnvironment:

    def __init__(self, quotes_streams: dict, fees: dict):
        # TODO:brandon.shute:2019-05-08: Error hanlde size of stream and fees
        self.__quotes_streams = quotes_streams
        self.__fees = fees

    def get_trading_decision_points(self) -> list:
        num_quotes = next(iter(self.__quotes_streams.values())).get_length()
        optima_flags = [self.__is_trading_decision_points(index) for index in range(num_quotes)]
        return list(filter(lambda x: optima_flags[x], range(num_quotes)))

    def __is_trading_decision_points(self, index: int) -> list:
        return any([self.__quotes_streams[instrument].get_local_optima_flags()[index] for instrument in self.__quotes_streams.keys()])

    def get_profit_and_loss_for_all(self, investment: float, buy_index: int, sell_index: int) -> dict:
        profit_and_loss = {}
        for instrument in self.__quotes_streams.keys():
            profit_and_loss[instrument] = self.get_profit_and_loss(investment, buy_index, sell_index, instrument)
        return profit_and_loss

    def get_profit_and_loss(self, investment: float, buy_index: int, sell_index: int, instrument: str) -> float:
        # TODO:brandon.shute:2019-05-08: Error handle indices and instrument
        # TODO:brandon.shute:2019-05-08: Cleanup
        return investment * (self.__quotes_streams[instrument].get_quote(sell_index).get_rate() - self.__quotes_streams[instrument].get_quote(buy_index).get_rate()) - self.__fees[instrument]

    def get_fee(self, instrument: str) -> float:
        return self.__fees[instrument]

    @staticmethod
    def from_csv(market_data_location: str, fee_location: str):
        market_data_df = pd.read_csv(market_data_location)
        fee_data_df = pd.read_csv(fee_location)
        market_data = {k: MarketDataStream(v) for k, v in  market_data_df.to_dict(orient='list').items()}
        fee_data = {k: v[0] for k, v in  fee_data_df.to_dict(orient='list').items()}
        return MarketEnvironment(market_data, fee_data)
