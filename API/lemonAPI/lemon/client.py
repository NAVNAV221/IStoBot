from lemon import api

from API.lemonAPI.lemon.consts import Tokens, General


class Client:
    def __init__(self, env: General.ENVIRONMENT_TYPING = General.INTEGRATION_ENV):
        self.client = api.create(
            market_data_api_token=Tokens.MARKET_DATA,
            trading_api_token=Tokens.PAPER_TRADING,
            env=env
        )


if __name__ == '__main__':
    c = Client()
    # get venues
    response = c.client.market_data.instruments.get(
        isin=["US88160R1014", "US0231351067"]
    )
    for res in response.results:
        print(res.symbol)
