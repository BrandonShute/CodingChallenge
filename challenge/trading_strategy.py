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
        for i in range(len(decision_points)):
            buy_index = decision_points[i]
            sell_index = decision_points[i + 1]
            self.__portfolio_value += self.__execute_trade(buy_index, sell_index)

    def __execute_trade(self, buy_index: int, sell_index: int) -> float:
        profits = filter(
            lambda x: x > 0,
            self.__market_env.get_profit_and_loss_for_all(self.__portfolio_value, buy_index, sell_index)
        )
        # Sell out of position and do nothing
        if len(profits) == 0:
            self.__current_instrument = None
        # Execute the best trade (could be to hold)
        else:
            best_instrument = max(profits.iteritems(), key=operator.itemgetter(1))[0]
            profit = profits[best_instrument]
            # No fees if holding the same instrument
            if best_instrument == self.__current_instrument:
                profit += self.__market_env.get_fee(self.__current_instrument)
            else:
                self.__current_instrument = best_instrument


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception(
           "Expected 2 arguments (market data file and fee file) but " +
           len(sys.argv) + " were received!"
        )
    market_data_location = sys.argv[0]
    fee_location = sys.argv[0]
    trading_strategy = TradingStrategy(
        INVESTMENT,
        MarketEnvironment.from_csv(market_data_location, fee_location)
    )
    trading_strategy.execute_optimal_strategy()
    print("The optimal PnL was determined to be: " + trading_strategy.get_portfolio_value())
