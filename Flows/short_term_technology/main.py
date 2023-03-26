from time import sleep
from typing import List

from Alerts.sms.sms import Sms
from consts.alerts.sms import System, Templates
from filters.screener.platforms.finviz_platform import FinvizScreener


def cron_job(seconds=5):
    def job(func):
        def wrapper(*args, **kwargs):
            while True:
                print('Start execute function ...')
                func(*args, **kwargs)
                print(f'Finish execution ...')
                sleep(seconds)

        return wrapper

    return job


@cron_job(seconds=43200)
def main():
    scanner = FinvizScreener()
    alert = Sms()
    TEST_PHONE_NUMBER = '972526368078'

    matched_scanner_tickers: List[str] = scanner.get_matched_tickers()
    print(f'matched_scanner_tickers: {matched_scanner_tickers}')
    alert_data = Templates.MATCHED_TICKERS_SMS.format(username='Nave', filters=scanner.format_filters(),
                                                      matched_wanted_tickers=matched_scanner_tickers)

    alert.send_sms(body=alert_data, sender=System.SENDER,
                   receiver=System.RECEIVER.format(phone_number=TEST_PHONE_NUMBER))
    print(f'Message sent')


if __name__ == '__main__':
    main()
