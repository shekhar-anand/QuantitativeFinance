"""
Constants used in the modules
Don't change these values. It might break the code.
"""
import logging
from enum import Enum

default = "null"
log_level = logging.DEBUG


class ChartType(Enum):
    """
    This class defines the type of chart in ChartElement object
    """
    CANDLESTICK = "candlestick"
    LINE = 'line'
    COLUMN = 'column'
    JUMPLINE = 'jumpLine'

    def __str__(self):
        return self.value


class ChartAxis(Enum):
    """
    This class defines the chart axis in ChartElement object
    """
    SAME_AXIS = 0
    DIFFERENT_AXIS = 1

    def __str__(self):
        return str(self.value)


class Operation(Enum):
    """
    This class is used to define operation for data in a Condition Object
    """
    EQUAL = "="
    GREATER_THAN_EQUAL = ">="
    LESS_THAN_EQUAL = "<="
    GREATER_THAN = ">"
    LESS_THAN = "<"
    CROSSOVER = "CROSSOVER"
    CROSSUNDER = "CROSSUNDER"
    RANGE_EQUAL = "<=  <="
    # These are used with patterns only
    BULL_RANGE = [1, 100]
    BEAR_RANGE = [-1, -100]

    def __str__(self):
        return self.value


class ChartColor(Enum):
    """
    This class defines the color of element in ChartElement object
    """
    RED = 'RED'
    BLUE = 'BLUE'
    GREEN = 'GREEN'
    YELLOW = 'YELLOW'
    PINK = 'PINK'
    PURPLE = 'PURPLE'

    def __str__(self):
        return self.value


class Logical(Enum):
    """
    This class is used to define logical operation between two Condition Objects
    in ConditionLogic object
    """
    AND = "&"
    OR = "|"

    def __str__(self):
        return self.value


class Pattern(Enum):
    """
    Pattern Keys for pattern hunter
    """
    two_crows = "CDL2CROWS"
    three_black_crows = "CDL3BLACKCROWS"
    three_advancing_black_soldiers = "CDL3WHITESOLDIERS"
    closing_marubozu = "CDLCLOSINGMARUBOZU"
    dark_cloud_cover = "CDLDARKCLOUDCOVER"
    doji = "CDLDOJI"
    doji_star = "CDLDOJISTAR"
    dragonfly_doji = "CDLDRAGONFLYDOJI"
    engulfing_pattern = "CDLENGULFING"
    evening_star = "CDLEVENINGSTAR"
    gravestone_doji = "CDLGRAVESTONEDOJI"
    hammer = "CDLHAMMER"
    hanging_man = "CDLHANGINGMAN"
    harami_pattern = "CDLHARAMI"
    harami_cross_pattern = "CDLHARAMICROSS"
    inverted_hammer = "CDLINVERTEDHAMMER"
    marubozu = "CDLMARUBOZU"
    morning_doji_star = "CDLMORNINGDOJISTAR"
    morning_star = "CDLMORNINGSTAR"
    shooting_star = "CDLSHOOTINGSTAR"
    spinning_top = "CDLSPINNINGTOP"
    tasuki_gap = "CDLTASUKIGAP"
    upside_gap_two_crows = "CDLUPSIDEGAP2CROWS"

    def __str__(self):
        return self.value


class Keys:
    daily = 'daily'
    weekly = 'weekly'
    monthly = 'monthly'
    yearly = 'yearly'
    interval = 'interval'
    scrip = 'scrip'
    symbol = 'symbol'
    size = 'size'
    start_date = 'start_date'
    end_date = 'end_date'
    chart = 'chart'
    bt_chart = 'bt_chart'
    date = 'date'
    open = 'open'
    high = 'high'
    low = 'low'
    close = 'close'
    volume = 'volume'
    turnover = 'turnover'

    data_prop = 'data_properties'
    data = 'data'
    params = 'params'

    rsi = "RSI"
    stoch = "STOCH"
    fastk = "fastk"
    fastd = "fastd"
    sma = "SMA"
    ema = "EMA"
    macd = "MACD"
    macd_value = "macd_value"
    macdsignal = "macdsignal"
    macdhist = "macdhist"
    bbands = "BBANDS"
    upperband = "upperband"
    middleband = "middleband"
    lowerband = "lowerband"
    pivot = "PIVOT"
    pp = "pp"
    r1 = "r1"
    r2 = "r2"
    r3 = "r3"
    s1 = "s1"
    s2 = "s2"
    s3 = "s3"
    data_min = "data_min"
    data_max = "data_max"
    pivot_min = "pivot_min"
    pivot_max = "pivot_max"

    signal = 'Signal'
    quantity = 'QTY'
    price = 'Price'
    pl = 'P_L'
    cum_pl = 'CUM_P_L'
    date_cum_pl = 'DATE_CUM_PL'
    patterns = "patterns"
    all = 'all'
    long = 'long'
    short = 'short'
    annotations = 'annotations'
    buy_regular = "BR"
    buy_book_profit = "BP"
    buy_book_sl = "BSL"
    sell_regular = "SR"
    sell_book_profit = "SP"
    sell_book_sl = "SSL"
