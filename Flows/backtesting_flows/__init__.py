"""
Flows intended to use by 'backtest' to check whether we succeed or not with our strategy trade from stock's previous data.

'backtest':
An iteration over stock's history data, that decide whether to buy the symbol or not based on our strategy.
The iteration done on stock's open and close points.

Example:
    func strategy_A(symbol):
        if symbol.sma_100 > symbol.sma_200:
            return True
        else:
            return False

    func backtest(strategy):
        symbol = 'TSLA'

        for(date(2019-01-01) -> date(2023-04-21)):
            symbol_data = current_symbol_data(symbol, start_date, end_date)
            if strategy(symbol_data):
                self.buy()
            else:
                self.sell()
    backtest(strategy_A)

An iteration on trading strategy that take a Symbol and check the strategy's result on symbol between certain date range.

These kind of flows special because we use stock's data (Close, Open price) only from specific date range.
"""
