from bot.flows.flow import Flow
from bot.filters.screener.platforms.finviz_platform import FinvizScreener


class EranFlow(Flow):
    FINVIZ_CHANNEL_DOUBLE_BOTTOM_SCREENER_PROPERTIES = {
        'filter_type': {
            'screener': {
                'screener_platform': 'FINVIZ',
                'filters': {
                    'Pattern': 'Double Bottom'
                }
            }
        }
    }

    FINVIZ_CHANNEL_DOUBLE_TOP_SCREENER_PROPERTIES = {
        'filter_type': {
            'screener': {
                'screener_platform': 'FINVIZ',
                'filters': {
                    'Pattern': 'Double Top'
                }
            }
        }
    }

    FINVIZ_CHANNEL_UP_SCREENER_PROPERTIES = {
        'filter_type': {
            'screener': {
                'screener_platform': 'FINVIZ',
                'filters': {
                    'Pattern': 'Channel Up'
                }
            }
        }
    }

    def run(self):
        channel_up_screener = set(FinvizScreener(
            input_data=EranFlow.FINVIZ_CHANNEL_UP_SCREENER_PROPERTIES).get_matched_tickers())
        double_top_screener = set(FinvizScreener(
            input_data=EranFlow.FINVIZ_CHANNEL_DOUBLE_TOP_SCREENER_PROPERTIES).get_matched_tickers())
        double_bottom_screener = set(FinvizScreener(
            input_data=EranFlow.FINVIZ_CHANNEL_DOUBLE_BOTTOM_SCREENER_PROPERTIES).get_matched_tickers())

        self.logger.info(f"len(channel_up_screener): {len(channel_up_screener)}")
        self.logger.info(f"len(double_top_screener): {len(double_top_screener)}")
        self.logger.info(f"len(double_bottom_screener): {len(double_bottom_screener)}")

        channel_up_double_top_stock: set = channel_up_screener.intersection(double_top_screener)
        self.logger.info(f"channel_up_screener intersect double_top_screener length: {channel_up_double_top_stock}")
        channel_up_double_bottom_stock: set = channel_up_screener.intersection(double_bottom_screener)
        self.logger.info(
            f"channel_up_screener intersect double_bottom_screener length: {channel_up_double_bottom_stock}")

        matched_scanner_tickers: set = channel_up_double_top_stock.union(channel_up_double_bottom_stock)
        self.logger.info(f'matched_scanner_tickers: {matched_scanner_tickers}')

        # alert = Sms()
        # client = Client()
        # QUANTITY_PER_STOCK = 10
        # TEST_PHONE_NUMBER = '972526368078'
        #
        # self.logger.info(f'Start buying process ...')
        #
        # filters = {
        #     'filters': {
        #         'Pattern': ['Double Top', 'Double Bottom', 'Channel Up'],
        #     }
        # }
        # alert_sms_data = Templates.MATCHED_TICKERS_SMS.format(username='Nave',
        #                                                       filters=filters,
        #                                                       matched_wanted_tickers=matched_scanner_tickers)
        #
        # alert.send_sms(body=alert_sms_data, sender=System.SENDER,
        #                receiver=System.RECEIVER.format(phone_number=TEST_PHONE_NUMBER))
        # self.logger.info(f'Message sent')
        #
        # for ticker in matched_scanner_tickers:
        #     s = Symbol(ticker=ticker)
        #
        #     try:
        #         client.buy_stock(symbol=s, quantity=QUANTITY_PER_STOCK)
        #         self.logger.info(f'Buy {QUANTITY_PER_STOCK} units from ticker: {ticker}')
        #
        #         buy_sms_data = Templates.BUYING_ACTION_SMS.format(ticker=ticker, units=QUANTITY_PER_STOCK)
        #         alert.send_sms(body=buy_sms_data, sender=System.SENDER,
        #                        receiver=System.RECEIVER.format(phone_number=TEST_PHONE_NUMBER))
        #         self.logger.info(f'Message sent')
        #
        #     except Exception as err:
        #         self.logger.info(f'Cant buy stock according to the following errors: {err}')
        #

if __name__ == '__main__':
    s = EranFlow()
    s.run()