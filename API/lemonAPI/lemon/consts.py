from typing import Literal


class General:
    INTEGRATION_ENV = 'paper'
    ENVIRONMENT_TYPING = Literal["paper", "money", "live"]


class Tokens:
    PAPER_TRADING = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJsZW1vbi5tYXJrZXRzIiwiaXNzIjoibGVtb24ubWFya2V0cyIsInN1YiI6InVzcl9yeUZoWTk5dHRiZDNRQmcyQjBrTGQzNmNkTFhyMzl6TmtXIiwiZXhwIjoxNzExMzk2MjM3LCJpYXQiOjE2Nzk4NjAyMzcsImp0aSI6ImFwa19yeUZoWTk5eHhGM0g5cUR0TkJkTmRSQlJIWmJwNDl5ejU4IiwibW9kZSI6InBhcGVyIn0.rf1RlUJVH2fduC-h3Qx-FtQEFE6u9pZfdEuUnRZaTig'
    MARKET_DATA = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJsZW1vbi5tYXJrZXRzIiwiaXNzIjoibGVtb24ubWFya2V0cyIsInN1YiI6InVzcl9yeUZoWTk5dHRiZDNRQmcyQjBrTGQzNmNkTFhyMzl6TmtXIiwiZXhwIjoxNzExMzk2MjM3LCJpYXQiOjE2Nzk4NjAyMzcsImp0aSI6ImFwa19yeUZoWTk5eHhza0NYRjlYcURueUYwdGJOMzMzZjI3bXpTIiwibW9kZSI6InBhcGVyIn0.MPFGQB6bMCd5gEGZ38Slf64szp-_QvmGU15YAKCX4_0'


class RequestsAPI:
    ORDER = 'https://paper-trading.lemon.markets/v1/orders'
    INSTRUMENTS = 'https://data.lemon.markets/v1/instruments/'
