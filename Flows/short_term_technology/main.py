from typing import List

from Alerts.sms.sms import Sms
from Flows.flow import Flow
from Logics.bear_market.is_bear_market import BearMarketLogic
from consts.alerts.sms import System, Templates
from filters.screener.platforms.finviz_platform import FinvizScreener


class ShortTermTechnologyFlow(Flow):
    FINVIZ_SCREENER_SHORT_TERM_PROPERTIES = {'filter_type': {'screener': {'screener_platform': 'FINVIZ', 'filters': {
        'Market Cap.': '+Small (over $300mln)', '20-Day Simple Moving Average': 'Price above SMA20',
        '50-Day Simple Moving Average': 'Price above SMA50', 'Sales growthpast 5 years': 'Over 10%',
        'Average Volume': 'Over 500K', 'Relative Volume': 'Over 1.5', 'Pattern': 'Horizontal S/R', 'Country': 'USA'}}}}

    def run(self):
        bear_market_logic = BearMarketLogic()
        scanner = FinvizScreener(input_data=ShortTermTechnologyFlow.FINVIZ_SCREENER_SHORT_TERM_PROPERTIES)
        alert = Sms()
        TEST_PHONE_NUMBER = '972526368078'

        is_bear_market: bool = bear_market_logic.run(market_ticker='SPY')

        if not is_bear_market:
            matched_scanner_tickers: List[str] = scanner.get_matched_tickers()
            self.logger(f'matched_scanner_tickers: {matched_scanner_tickers}')
            alert_data = Templates.MATCHED_TICKERS_SMS.format(username='Nave', filters=scanner.format_filters(),
                                                              matched_wanted_tickers=matched_scanner_tickers)

            alert.send_sms(body=alert_data, sender=System.SENDER,
                           receiver=System.RECEIVER.format(phone_number=TEST_PHONE_NUMBER))
            self.logger(f'Message sent')


if __name__ == '__main__':
    s = ShortTermTechnologyFlow()
    s.run()
