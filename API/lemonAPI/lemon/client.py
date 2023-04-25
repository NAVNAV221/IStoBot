from datetime import datetime
from typing import List

from lemon import api
from lemon.market_data.model import Instrument

from API.lemonAPI.lemon.consts import Tokens, General
from utils.project_logger import get_logger


class Client:
    def __init__(self, env: General.ENVIRONMENT_TYPING = General.INTEGRATION_ENV):
        self.client = api.create(
            market_data_api_token=Tokens.MARKET_DATA,
            trading_api_token=Tokens.PAPER_TRADING,
            env=env
        )
        self.logger = get_logger()

    def _map_symbol_to_isin(self, symbol: str) -> str:
        """
        Map ISIN number to symbol.
        :param symbol:
        :return:
        """
        response = self.client.market_data.instruments.get(search=symbol)

        if response.results:
            instrument_options: List[Instrument] = [result for result in response.results]
            self.logger.info(f"Found the following company during symbol to isin mapping: {instrument_options}")

            isin = instrument_options[0].isin
            self.logger.info(f"Chosen isin: {isin}")
            return isin

        raise Exception(f"Cant find ISIN for symbol: {symbol}")

    def buy_stock(self, stock_isin: str, quantity: int, index: str):
        buy_expires_at = datetime.fromisoformat("2023-04-28")

        response = self.client.trading.orders.create(
            isin=stock_isin,
            side='buy',
            quantity=quantity,
            expires_at=buy_expires_at
        )

        order_id = response.results.id

        return order_id


if __name__ == '__main__':
    c = Client()
    symbol = 'APPLE'
    stock_isin = c._map_symbol_to_isin(symbol=symbol)
    c.buy_stock(stock_isin=stock_isin, quantity=50, index='SPY')
    #
    # import requests
    # import json
    #
    # paper_trading_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJsZW1vbi5tYXJrZXRzIiwiaXNzIjoibGVtb24ubWFya2V0cyIsInN1YiI6InVzcl9yeUZoWTk5dHRiZDNRQmcyQjBrTGQzNmNkTFhyMzl6TmtXIiwiZXhwIjoxNzExMzk2MjM3LCJpYXQiOjE2Nzk4NjAyMzcsImp0aSI6ImFwa19yeUZoWTk5eHhGM0g5cUR0TkJkTmRSQlJIWmJwNDl5ejU4IiwibW9kZSI6InBhcGVyIn0.rf1RlUJVH2fduC-h3Qx-FtQEFE6u9pZfdEuUnRZaTig'
    # request = requests.post("https://paper-trading.lemon.markets/v1/orders",
    #                         data=json.dumps({
    #                             "isin": "US19260Q1076",
    #                             "expires_at": "2023-04-28",
    #                             "side": "buy",
    #                             "quantity": 1,
    #                             "venue": "XMUN",
    #                         }),
    #                         headers={"Authorization": f"Bearer {paper_trading_key}"})
    # print(request.json())
