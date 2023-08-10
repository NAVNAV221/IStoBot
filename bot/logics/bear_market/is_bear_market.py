from datetime import datetime
from bot.logics import Logic
from bot.logics.sub_logic_utils.ticker_percentage_from_bottom import TickerPercentageFromBottom


class BearMarketLogic(Logic):
    def main(self, market_ticker: str, start_date: datetime, end_date: datetime) -> bool:
        t = TickerPercentageFromBottom()
        market_price_percent_from_highest = t.run(market_ticker=market_ticker, start_date=start_date, end_date=end_date)

        if market_price_percent_from_highest > 120:
            self.logger.info(f'Bear market with market_price_percent_from_highest: {market_price_percent_from_highest}')
            return True

        self.logger.info(f'Not bear market with market_price_percent_from_highest: {market_price_percent_from_highest}')
        return False


if __name__ == '__main__':
    b = BearMarketLogic()
    b.run(market_ticker='SPY')
