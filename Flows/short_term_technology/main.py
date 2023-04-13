from typing import List

from Alerts.sms.sms import Sms
from Flows.flow import Flow
from Logics.bear_market.is_bear_market import BearMarketLogic
from consts.alerts.sms import System, Templates
from filters.screener.platforms.finviz_platform import FinvizScreener


class ShortTermTechnologyFlow(Flow):
    def run(self):
        bear_market_logic = BearMarketLogic()
        scanner = FinvizScreener()
        alert = Sms()
        TEST_PHONE_NUMBER = '972526368078'

        is_bear_market: bool = bear_market_logic.run(ticker='SPY')

        if is_bear_market:
            matched_scanner_tickers: List[str] = scanner.get_matched_tickers()
            self.logger(f'matched_scanner_tickers: {matched_scanner_tickers}')
            alert_data = Templates.MATCHED_TICKERS_SMS.format(username='Nave', filters=scanner.format_filters(),
                                                              matched_wanted_tickers=matched_scanner_tickers)

            alert.send_sms(body=alert_data, sender=System.SENDER,
                           receiver=System.RECEIVER.format(phone_number=TEST_PHONE_NUMBER))
            self.logger(f'Message sent')
