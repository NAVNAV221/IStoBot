from typing import List
from datetime import datetime, timedelta

from API.alpacaAPI.client import Client
from API.yfinanceAPI.yfinance.symbol import Symbol
from bot.Alerts.sms.sms import Sms
from bot.flows.flow import Flow
from bot.logics.bear_market.is_bear_market import BearMarketLogic
from consts.alerts.sms import System, Templates
from bot.filters.screener.platforms.finviz_platform import FinvizScreener


class ShortTermTechnologyFlow(Flow):
    FINVIZ_SCREENER_SHORT_TERM_PROPERTIES = {'filter_type': {'screener': {'screener_platform': 'FINVIZ', 'filters': {
        'Market Cap.': '+Small (over $300mln)', '20-Day Simple Moving Average': 'Price above SMA20',
        '50-Day Simple Moving Average': 'Price above SMA50', 'Sales growthpast 5 years': 'Over 10%',
        'Average Volume': 'Over 500K', 'Relative Volume': 'Over 1.5', 'Pattern': 'Horizontal S/R', 'Country': 'USA'}}}}

    def run(self, start_date: datetime, end_date: datetime):
        bear_market_logic = BearMarketLogic()

        scanner = FinvizScreener(input_data=ShortTermTechnologyFlow.FINVIZ_SCREENER_SHORT_TERM_PROPERTIES)
        alert = Sms()
        client = Client()
        QUANTITY_PER_STOCK = 10
        TEST_PHONE_NUMBER = '972526368078'

        is_bear_market: bool = bear_market_logic.run(market_ticker='SPY', start_date=start_date, end_date=end_date)

        if not is_bear_market:
            matched_scanner_tickers: List[str] = scanner.get_matched_tickers()
            self.logger.info(f'matched_scanner_tickers: {matched_scanner_tickers}')
            self.logger.info(f'Start buying process ...')

            alert_sms_data = Templates.MATCHED_TICKERS_SMS.format(username='Nave',
                                                                  filters=scanner.format_filters(),
                                                                  matched_wanted_tickers=matched_scanner_tickers)

            alert.send_sms(body=alert_sms_data, sender=System.SENDER,
                           receiver=System.RECEIVER.format(phone_number=TEST_PHONE_NUMBER))
            self.logger.info(f'Message sent')

            for ticker in matched_scanner_tickers:
                s = Symbol(ticker=ticker)

                try:
                    client.buy_stock(symbol=s, quantity=QUANTITY_PER_STOCK)
                    self.logger.info(f'Buy {QUANTITY_PER_STOCK} units from ticker: {ticker}')

                    buy_sms_data = Templates.BUYING_ACTION_SMS.format(ticker=ticker, units=QUANTITY_PER_STOCK)
                    alert.send_sms(body=buy_sms_data, sender=System.SENDER,
                                   receiver=System.RECEIVER.format(phone_number=TEST_PHONE_NUMBER))
                    self.logger.info(f'Message sent')

                except Exception as err:
                    self.logger.info(f'Cant buy stock according to the following errors: {err}')


if __name__ == '__main__':
    start_date = datetime.now() - timedelta(days=14)
    end_date = datetime.now()

    s = ShortTermTechnologyFlow()
    s.run(start_date=start_date, end_date=end_date)
