from datetime import datetime, timedelta

from bot.filters.screener.platforms.finviz_platform import FinvizScreener
from bot.flows.flow import Flow
from core.components.symbol import Symbol
from core.components.symbol.utils.doubles import get_last_double_buttom, get_last_double_top


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

    FINVIZ_NORMAL_PRICE_SCREENER_PROPERTIES = {
        'filter_type': {
            'screener': {
                'screener_platform': 'FINVIZ',
                'filters': {
                    'Price': 'Over $30'
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
        normal_price_screener = set(FinvizScreener(
            input_data=EranFlow.FINVIZ_NORMAL_PRICE_SCREENER_PROPERTIES).get_matched_tickers())



        self.logger.info(f"len(channel_up_screener): {len(channel_up_screener)}")
        self.logger.info(f"len(double_top_screener): {len(double_top_screener)}")
        self.logger.info(f"len(double_bottom_screener): {len(double_bottom_screener)}")
        self.logger.info(f"len(normal_price_screener): {len(normal_price_screener)}")

        channel_up_double_top_stock: set = channel_up_screener.intersection(double_top_screener)
        self.logger.info(f"channel_up_screener intersect double_top_screener length: {channel_up_double_top_stock}")
        channel_up_double_bottom_stock: set = channel_up_screener.intersection(double_bottom_screener)
        self.logger.info(
            f"channel_up_screener intersect double_bottom_screener length: {channel_up_double_bottom_stock}")

        matched_scanner_tickers: set = channel_up_double_top_stock.union(channel_up_double_bottom_stock)
        # matched_scanner_tickers: set = matched_scanner_tickers.intersection(channel_up_double_bottom_stock)
        self.logger.info(f'matched_scanner_tickers: {matched_scanner_tickers}')

        for ticker in matched_scanner_tickers:
            s = Symbol(ticker=ticker, end_date=end_date, start_date=start_date)
        #
        #     double_buttom_candles = get_last_double_buttom(s)
        #     double_top_candles = get_last_double_top(s)
        #
        #     s.risk_reward_ratio(entry=s.price, stop=double_buttom_candles[0]['Close'], target=double_top_candles[0]['Close'])

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



if __name__ == '__main__':
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)

    s = EranFlow()
    s.run()
