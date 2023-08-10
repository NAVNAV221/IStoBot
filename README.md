# IStoBot

Helps you to be 100% aware of your stock with multiple tools:

* Alert mechanism.
* Smart usage of stock API.
* Stock information from any source.
* Act and notify on specific scenarios.

# Component

## Symbol

Should be accessible to all project's code functionalities. Here we get access to any APIs we'll want.

```python
from IStoBot import Symbol

appl = Symbol(ticker='AAPL')
```

# API

API sources we used to analyse the stock. Target is to make `symbol` component generic as possible to let users add APIs
as many as they want.

```python
    appl.api.yahoo.info.get('regularMarketPrice')
    appl.api.finvizAPI.get_ticker_details()
```

# Bot

Contain all non-user needed actions. Inside bot, we'll find:

## Logics

Trade flow creation require many complicated logics in the way.
For example:
- There is a bear market ?
- Number of bad words in symbol news grater then 10.
During trade method creation you'll use many APIs to get information from.

Each code logic found in this folder. We'll use them during symbol Flows and more ...
- [ ] Decide if Logic instance stay or not.
## Flows

We can create scenarios and act upon them; Alert via SMS, Suggest buying symbol and more ...

```python
from typing import List

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

    def run(self, phone_number):
        bear_market_logic = BearMarketLogic()
        scanner = FinvizScreener(input_data=ShortTermTechnologyFlow.FINVIZ_SCREENER_SHORT_TERM_PROPERTIES)
        alert = Sms()
        is_bear_market: bool = bear_market_logic.run(market_ticker='SPY')

        if not is_bear_market:
            matched_scanner_tickers: List[str] = scanner.get_matched_tickers()
            self.logger(f'matched_scanner_tickers: {matched_scanner_tickers}')
            alert_data = Templates.MATCHED_TICKERS_SMS.format(username='Nave', filters=scanner.format_filters(),
                                                              matched_wanted_tickers=matched_scanner_tickers)

            alert.send_sms(body=alert_data, sender=System.SENDER,
                           receiver=System.RECEIVER.format(phone_number=phone_number))
            self.logger(f'Message sent')


if __name__ == '__main__':
    s = ShortTermTechnologyFlow()
    s.run(phone_number='+123456')
```

- [ ] Schedule flow's run on server.

## Alerts

Alerts we want to use: SMS, Email and more ...

```python
alert.send_sms(body='hello from +1234', sender='+1234',
               receiver='+5678')
```

## Filters

During flow writing we filter unwanted companies by logic. Filter target is to get only relevant symbols and it'll do
that by:

* Screener
* News
* User custom choice

Those filters can get through JSON file input. Filter for example: Screener

- [ ] Build Pub/Sub system for each filter type

Filter object responsible to direct each request to it's relevant filter type.

### JSON request template

```json
{
  "filter_type": {
    "<filter system types>": {
      "<filter system key 1>": "<filter system value 1>",
      "<filter system key 2>": "<filter system value 2>"
    }
  }
}
```

### Filter Types

#### Screener

Screener serve investors to

```python
from filters.screener.platforms.finviz_platform import FinvizScreener

FINVIZ_SCREENER_SHORT_TERM_PROPERTIES = {'filter_type': {'screener': {'screener_platform': 'FINVIZ', 'filters': {
    'Market Cap.': '+Small (over $300mln)', '20-Day Simple Moving Average': 'Price above SMA20',
    '50-Day Simple Moving Average': 'Price above SMA50', 'Sales growthpast 5 years': 'Over 10%',
    'Average Volume': 'Over 500K', 'Relative Volume': 'Over 1.5', 'Pattern': 'Horizontal S/R', 'Country': 'USA'}}}}
scanner = FinvizScreener(input_data=FINVIZ_SCREENER_SHORT_TERM_PROPERTIES)
print(scanner.get_matched_tickers())
```

# Server

If we want to create system that based on those logics we need server to parse our requests.

```python
import requests

requests.post('http://localhost/filters/screener?platform=finviz', json=FINVIZ_SCREENER_SHORT_TERM_PROPERTIES)
```
