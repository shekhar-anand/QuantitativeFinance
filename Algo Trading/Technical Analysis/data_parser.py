import calendar
import logging
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

import quandl

import api
import pattern_hunter
from api import NSEFO
from model import *

_logger = logging.getLogger("data_parser")


def get_data(symbol: Symbol = NSEFO.NIFTY50, start_date: str = api.min_date, end_date: str = "",
             interval: str = Keys.daily, index:bool=True):
    """
    This is base function which extracts data from Quandl in a DataObject
    :param symbol: Symbol
                Scrip for which data is required. An Instance of api.Symbol class
    :param start_date: str
                Starting date for data. For e.g. '2017-08-08'
    :param end_date: str
                End date for data. For e.g. '2018-08-08'
    :param interval: str
                Data Interval for the scrip.
                Currently supports daily, weekly, monthly and yearly formats.
    :param index: bool
                Whether the
    :return: tuple
            data_properties: dict
                        Contains info about the data fetched from Quandl API. Such as scrip, start date etc.
            data: list[DataObject]
    """
    data = []
    date_fmt = '%Y-%m-%d'
    # quandl.ApiConfig.api_key = api.quandl_api_key
    # response = quandl.get(symbol.api_key, returns="numpy", start_date=start_date, end_date=end_date)
    # for i in range(len(response)):
    #     item = response[i]
    #     data.append(DataObject(item))

    from nsepy import get_history
    import numpy as np

    start = datetime.strptime(start_date, date_fmt).date()
    end = datetime.strptime(end_date, date_fmt).date() if end_date else datetime.now().date()
    response = get_history(symbol=symbol.scrip, start=start, end=end, index=index)

    dates = [np.datetime64(_date) for _date in response.index.values]
    open_data = response['Open'].values
    high = response['High'].values
    low = response['Low'].values
    close = response['Close'].values
    volume = response['Volume'].values
    turnover = response['Turnover'].values

    for _data in zip(dates, open_data, high, low, close, volume, turnover):
        # noinspection PyTypeChecker
        data.append(DataObject(_data))

    data_properties = {Keys.scrip: symbol.scrip,
                       Keys.start_date: start_date,
                       Keys.end_date: end_date,
                       Keys.chart: "%s" % ChartType.CANDLESTICK,
                       Keys.size: symbol.size}

    if interval == Keys.daily:
        data_properties.update({Keys.interval: Keys.daily})
        return data_properties, data
    elif interval == Keys.weekly:
        data_properties.update({Keys.interval: Keys.weekly})
        data = get_weekly_data(data)
        return data_properties, data
    elif interval == Keys.monthly:
        data_properties.update({Keys.interval: Keys.monthly})
        data = get_monthly_data(data)
        return data_properties, data
    elif interval == Keys.yearly:
        data_properties.update({Keys.interval: Keys.yearly})
        data = get_yearly_data(data)
        return data_properties, data
    else:
        data_properties.update({Keys.interval: interval})
        return data_properties, data

def get_weekly_data(data: list):
    """
    Weekly data from list[DataObject]
    :param data: list[DataObject]
    :return: list[DataObject]
    """
    candle_dates = []
    data_arr = []
    week_delta = relativedelta(weeks=1)
    first_date = data[0].date
    last_date = data[-1].date
    while first_date < last_date:
        weekday = first_date.isocalendar()
        back_time = timedelta(days=weekday[2] - 1)
        forward_time = timedelta(days=6)
        week_first = first_date - back_time
        week_last = week_first + forward_time
        candle_dates.append([week_first, week_last])
        first_date = first_date + week_delta
    for dates in candle_dates:
        month_date, open, high, low, close, volume, turnover = [], [], [], [], [], [], []
        for i in range(len(data)):
            if dates[0] <= data[i].date <= dates[1]:
                month_date.append(data[i].date)
                open.append(data[i].open)
                high.append(data[i].high)
                low.append(data[i].low)
                close.append(data[i].close)
                volume.append(data[i].volume)
                turnover.append(data[i].turnover)
        # month_date = dates[0]
        month_date = month_date[0]
        open = open[0]
        high = max(high)
        low = min(low)
        close = close[-1]
        volume = sum(volume)
        turnover = sum(turnover)
        obj = DataObject(**{Keys.date: month_date, Keys.open: open, Keys.high: high, Keys.low: low, Keys.close: close,
                            Keys.volume: volume, Keys.turnover: turnover})
        data_arr.append(obj)
    return data_arr


def get_monthly_data(data: list):
    """
    Monthly data from list[DataObject]
    :param data: list[DataObject]
    :return: list[DataObject]
    """
    candle_dates = []
    data_arr = []
    month_delta = relativedelta(months=1)
    first_date = data[0].date
    last_date = data[-1].date
    while first_date < last_date:
        days = calendar.monthrange(first_date.year, first_date.month)[1]
        candle_dates.append([date(year=first_date.year, month=first_date.month, day=1),
                             date(year=first_date.year, month=first_date.month, day=days)])
        first_date = first_date + month_delta
    for dates in candle_dates:
        month_date, open, high, low, close, volume, turnover = [], [], [], [], [], [], []
        for i in range(len(data)):
            if dates[0] <= data[i].date <= dates[1]:
                month_date.append(data[i].date)
                open.append(data[i].open)
                high.append(data[i].high)
                low.append(data[i].low)
                close.append(data[i].close)
                volume.append(data[i].volume)
                turnover.append(data[i].turnover)
        # month_date = dates[0]
        month_date = month_date[0]
        open = open[0]
        high = max(high)
        low = min(low)
        close = close[-1]
        volume = sum(volume)
        turnover = sum(turnover)
        obj = DataObject(**{Keys.date: month_date, Keys.open: open, Keys.high: high, Keys.low: low, Keys.close: close,
                            Keys.volume: volume, Keys.turnover: turnover})
        data_arr.append(obj)
    return data_arr


def get_yearly_data(data: list):
    """
    Yearly data from list[DataObject]
    :param data: list[DataObject]
    :return: list[DataObject]
    """
    candle_dates = []
    data_arr = []
    year_delta = relativedelta(years=1)
    first_date = data[0].date
    last_date = data[-1].date
    while first_date < last_date:
        candle_dates.append([date(year=first_date.year, month=1, day=1),
                             date(year=first_date.year, month=12, day=31)])
        first_date = first_date + year_delta
    for dates in candle_dates:
        year_date, open, high, low, close, volume, turnover = [], [], [], [], [], [], []
        for i in range(len(data)):
            if dates[0] <= data[i].date <= dates[1]:
                year_date.append(data[i].date)
                open.append(data[i].open)
                high.append(data[i].high)
                low.append(data[i].low)
                close.append(data[i].close)
                volume.append(data[i].volume)
                turnover.append(data[i].turnover)
        # month_date = dates[0]
        year_date = year_date[0]
        open = open[0]
        high = max(high)
        low = min(low)
        close = close[-1]
        volume = sum(volume)
        turnover = sum(turnover)
        obj = DataObject(**{Keys.date: year_date, Keys.open: open, Keys.high: high, Keys.low: low, Keys.close: close,
                            Keys.volume: volume, Keys.turnover: turnover})
        data_arr.append(obj)
    return data_arr


def get_ohlc(data: list = None):
    """
    When data is required in ohlc in list. This required for the pattern hunter operations.
    :param data: list[DataObject]
    :return: tuple
        A tuple containing open, high, low, close with each element as list.
    """
    if (data is None) | (data == []) | (type(data[0]) != DataObject):
        _logger.warning("Invalid data type in get_ohlc \nExpected %s got %s instead" % (DataObject, type(data[0])))
    else:
        open = numpy.asarray(get_open(data))
        high = numpy.asarray(get_high(data))
        low = numpy.asarray(get_low(data))
        close = numpy.asarray(get_close(data))
        return open, high, low, close


def get_date(data: list = None) -> list:
    """
    Get date from the list[DataObject]
    :param data: list[DataObject]
    :return: list
            A list containing only date
    """
    date_arr = []
    if (data is None) | (data == []):
        _logger.warning("Invalid data")
    else:
        for i in data:
            value = i.date
            date_arr.append(value)
    return date_arr


def get_open(data: list = None) -> list:
    """
    Get open from the list[DataObject]
    :param data: list[DataObject]
    :return: list
            A list containing only open
    """
    open = []
    if (data is None) | (data == []):
        _logger.warning("Invalid data")
    else:
        for i in data:
            value = i.open
            open.append(value)
    return open


def get_high(data: list = None):
    """
    Get high from the list[DataObject]
    :param data: list[DataObject]
    :return: list
            A list containing only high
    """
    high = []
    if (data is None) | (data == []):
        _logger.warning("Invalid data")
    else:
        for i in data:
            value = i.high
            high.append(value)
    return high


def get_low(data: list = None):
    """
    Get low from the list[DataObject]
    :param data: list[DataObject]
    :return: list
            A list containing only low
    """
    low = []
    if (data is None) | (data == []):
        _logger.warning("Invalid data")
    else:
        for i in data:
            value = i.low
            low.append(value)
    return low


def get_close(data: list = None):
    """
    Get close from the list[DataObject]
    :param data: list[DataObject]
    :return: list
            A list containing only close
    """
    close = []
    if (data is None) | (data == []):
        _logger.warning("Invalid data")
    else:
        for i in data:
            value = i.close
            close.append(value)
    return close


def get_volume(data: list = None):
    """
    Get volume from the list[DataObject]
    :param data: list[DataObject]
    :return: list
            A list containing only volume
    """
    volume = []
    if (data is None) | (data == []):
        _logger.warning("Invalid data")
    else:
        for i in data:
            value = i.volume
            volume.append(value)
    return volume


def get_turnover(data: list = None):
    """
    Get turnover from the list[DataObject]
    :param data: list[DataObject]
    :return: list
            A list containing only turnover
    """
    turnover = []
    if (data is None) | (data == []):
        _logger.warning("Invalid data")
    else:
        for i in data:
            value = i.turnover
            turnover.append(value)
    return turnover


def data_builder(data: list, data_properties: dict, charts: list = None, patterns: list = None):
    """
    Data builder is used to get data for charting.
    It formats data for charting of candle and indicators.
    :param data: list[DataObject]
    :param data_properties: dict
                Data properties returned from get_data function
    :param charts: list[ChartElement]
                A chart element contains data to be plotted on chart. For e.g. indicators
    :param patterns: list[Pattern]
                Patterns to be analysed for the given data
    :return: tuple
        A tuple of the form data_properties, params, data_list.
        data_properties: dict
                    All the properties related to the candle data
        params: list
                    All the properties related to the indicator or other than candle data
        data_list: list
                    A 2D list of data for charting
        pattern_data: list
                    A 2D list of date and high where pattern(s) is True
    """
    params = [Keys.date, Keys.open, Keys.high, Keys.low, Keys.close, Keys.volume]
    data_list = _append_data(data)
    indicators = []
    if charts is None:
        _logger.debug("No chart element specified")
    elif type(charts) == list:
        _logger.debug("Charts specified")
        for chart_element in charts:
            if type(chart_element) == ChartElement:
                parameter = "%s^%s^%s" % (
                    chart_element.type, chart_element.axis, chart_element.label)
                item = chart_element.data
                if type(item) == list:
                    _logger.debug("list")
                    params.append(parameter)
                    indicators.append(item)
                elif type(item) == dict:
                    _logger.debug('dict')
                    for key, value in item.items():
                        params.append("%s_%s" % (parameter, key))
                        indicators.append(value)
                else:
                    _logger.warning("Unknown data format or type")

    pattern_data = []
    if patterns is None:
        _logger.debug("No Pattern(s) specified")
    elif type(patterns) == list:
        _logger.debug("Pattern(s) specified")
        open, high, low, close = get_ohlc(data)
        dates = get_date(data)
        # noinspection PyTypeChecker
        pattern_data = _get_patterns(dates, open, high, low, close, patterns)
    else:
        _logger.warning("Patterns need to be given in a list")

    data_list = _append_indicators(indicators, data_list)
    _logger.debug("Params are: %s" % params)
    _logger.debug("Data properties: %s" % data_properties)
    return data_properties, params, data_list, pattern_data


def _append_data(data):
    """
    Helper function for data_builder.
    :param data: list[DataObject]
    :return: list
            A 2D list of candle data
    """
    result = []
    for child in data:
        if child.volume == ct.default:
            pass
        elif numpy.isnan(child.volume):
            child.volume = ct.default
        grand_child = ["%s-%s-%s 09:15:00" % (child.date.year, child.date.month, child.date.day), child.open,
                       child.high,
                       child.low, child.close, child.volume]
        result.append(grand_child)
    return result


def _append_indicators(indicators, father):
    """
    Helper function for data_builder
    :param indicators: list
                A list of  data for the indicators to be plotted on chart
    :param father: list
                Data for candle charting
    :return: list
                A 2D list of data
    """
    for item in indicators:
        _logger.debug("Item: %s " % len(item))
        _logger.debug("Father: %s" % len(father))
        for i in range(len(father)):
            father[i].append(item[i])
    return father


def round_float(number: float) -> float:
    """
    Round the float to two decimal precision.
    :param number: float
    :return: float
    """
    return float(Decimal(number).quantize(PRECISION))


def _get_patterns(dates: list, open: list, high: list, low: list, close: list, pattern: Union[Pattern, list]) -> list:
    """
    Evaluate patterns and return data for charting
    :param dates: list
                list[date]
    :param open: list
                list[numeric]
    :param high: list
                list[numeric]
    :param low: list
                list[numeric]
    :param close: list
                list[numeric]
    :param pattern: Union[Pattern, list]
                Pattern or Patterns to be analysed along with the strategy. If a pattern is bullish and
                Strategy is BUY then we will give a signal for a buy and similarly for SELL strategy and
                bearish pattern sell signal will be generated.
    :return: list
    """
    pattern_values, result = [], []
    max_range, min_range = 100, -100
    if type(pattern) == list:
        for item in pattern:
            if type(item) == Pattern:
                y = pattern_hunter.pattern_hunter(open, high, low, close, item)
                pattern_values.append(y)
            else:
                _logger.warning("Expected a type of %s got %s instead" % (type(Pattern), type(item)))
    else:
        _logger.debug("Invalid input in patterns for strategy_builder")
        _logger.warning("Expected a list type of %s got %s instead" % (Pattern, type(pattern)))

    for i in range(len(pattern_values)):
        pattern_result = pattern_values[i]
        name = pattern[i].name
        # name_arr = name.split("_")
        # x = ""
        # for name_element in name_arr:
        #     x += name_element[0]
        # name = x
        for j in range(len(pattern_result)):
            val = False
            m = pattern_result[j]
            if m == 0:
                val = False
            elif min_range <= m <= max_range:
                val = True

            if val is True:
                result.append(["%s-%s-%s" % (dates[j].year, dates[j].month, dates[j].day), high[j], name])
    return result
