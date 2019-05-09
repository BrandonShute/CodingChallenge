import sys
import operator
from domain.market_environment import MarketEnvironment

INVESTMENT = 100000


class TradingStrategy:

    def __init__(self, portfolio_value: float, market_env: MarketEnvironment):
        self.__portfolio_value = portfolio_value
        self.__market_env = market_env
        self.__current_instrument = None

    def get_portfolio_value(self):
        return self.__portfolio_value

    def execute_optimal_strategy(self):
        decision_points = self.__market_env.get_trading_decision_points()
        for i in range(len(decision_points) - 1):
            buy_index = decision_points[i]
            sell_index = decision_points[i + 1]
            self.__portfolio_value += self.__execute_trade(buy_index, sell_index)

    def __execute_trade(self, buy_index: int, sell_index: int) -> float:
        profit_and_losses = self.__market_env.get_profit_and_loss_for_all(self.__portfolio_value, buy_index, sell_index)
        # Add back the fee if holding the current instrument
        if self.__current_instrument is not None:
            profit_and_losses[self.__current_instrument] += self.__market_env.get_fee(self.__current_instrument)

        best_instrument = max(profit_and_losses.items(), key=operator.itemgetter(1))[0]
        max_profit = profit_and_losses[best_instrument]

        # Sell out of position and do nothing
        if max_profit <= 0:
            self.__current_instrument = None
            return 0.0

        self.__current_instrument = best_instrument
        return max_profit

if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise Exception(
           "Expected 2 optional arguments (market data file and fee file) but " +
           str(len(sys.argv) - 1) + " were received!"
        )
    market_data_location = sys.argv[1]
    fee_location = sys.argv[2]
    trading_strategy = TradingStrategy(
        INVESTMENT,
        MarketEnvironment.from_csv(market_data_location, fee_location)
    )
    trading_strategy.execute_optimal_strategy()
    print("The optimal PnL was determined to be: " + str(trading_strategy.get_portfolio_value()))
