from alpaca.trading import OrderSide, TimeInForce
from alpaca.trading.client import TradingClient
from alpaca.trading.models import Order
from alpaca.trading.requests import MarketOrderRequest

from API.alpacaAPI.consts import Config, Environment
from API.yfinanceAPI.yfinance.symbol import Symbol


class Client:
    def __init__(self):
        self.trading_client = TradingClient(api_key=Config.API_KEY, secret_key=Config.SECRET_KEY,
                                            paper=Environment.INTEGRATION)

    def order_request(self, **kwargs) -> Order:
        """
        Make an order request
        :param kwargs: parameters to Alpaca order request
        :return: Order made by Alpaca.
        """

        order_details = MarketOrderRequest(**kwargs)
        order = self.trading_client.submit_order(order_data=order_details)

        return order

    def buy_stock(self, symbol: Symbol, quantity: int) -> Order:
        """
        Make an 'buy' order request
        :param symbol: 'TSLA'
        :param quantity: 15 units
        :return: Order object.
        """
        market_order_request_details = self.order_request(symbol=symbol.ticker, qty=quantity, side=OrderSide.BUY,
                                                          time_in_force=TimeInForce.DAY)

        return market_order_request_details


def test():
    c = Client()
    # print(c.trading_client.get_account())
    # c.order_request(symbol="SPY",
    #                 qty=100,
    #                 side=OrderSide.BUY,
    #                 time_in_force=TimeInForce.DAY)
    s = Symbol(ticker='SPY')
    c.buy_stock(symbol=s, quantity=10)


if __name__ == '__main__':
    test()
