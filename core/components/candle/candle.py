from dataclasses import dataclass
from datetime import datetime


@dataclass
class Candle:
    date: datetime
    high: float
    low: float
    open: float
    close: float
