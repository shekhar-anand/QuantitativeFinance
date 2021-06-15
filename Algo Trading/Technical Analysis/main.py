import numpy

import charting
import data_parser
import indicators
import strategy

from constants import Keys, ChartType, ChartAxis, Operation
from model import Pattern, ChartElement, Condition, ConditionsLogic, Logical
from strategy import Strategies

if __name__ == '__main__':
    # TODO: Begin from here
    data_prop, data = data_parser.get_data(start_date="2012-03-01", interval=Keys.daily)
    high = data_parser.get_high(data)
    low = data_parser.get_low(data)
    close = data_parser.get_close(data)
    # TODO: 1. Define the indicators to be used in the strategy
    sma = indicators.sma(close)
    ema = indicators.ema(close)
    rsi = indicators.rsi(close)
    macd = indicators.macd(close)
    stoch = indicators.stoch(high, low, close)
    bbands = indicators.bollinger_bands(close)
    pivot = indicators.pivot(data, interval=Keys.monthly)
    pivot1 = indicators.pivot(data, interval=Keys.weekly)
    pivot2 = indicators.pivot(data, interval=Keys.daily)

    # TODO: 2. Define conditions for the strategy optimizations
    buy1 = Condition(data1=ema, data2=sma, operation=Operation.CROSSOVER)
    buy2 = Condition(data1=[Pattern.closing_marubozu], data2=[50, 100])
    buy = ConditionsLogic(condition1=buy1, condition2=buy2, logical=Logical.OR)
    sell_1 = Condition(data1=ema, data2=sma, operation=Operation.CROSSUNDER)
    sell_2 = Condition(data1=[Pattern.doji_star], operation=Operation.BEAR_RANGE)

    # TODO: 3. Optimize the strategy using following methods
    strategy.strategy_optimizations(data_properties=data_prop, data_list=data, buy=buy,
                                    sell=[sell_1, sell_2], target_range=[1.0, 1.3, 1.9, 2.2, 2.5, 3, 3.5, 4],
                                    sl_range=[0.3, 0.5, 0.6, 0.8, 1,1,1,1], strategy=strategy.BUY, strategy_name="list")
    # strategy.strategy_optimizationsptimizations(data_properties=data_prop, data_list=data, buy=buy,
    #                                 sell=[sell_1, sell_2], target_range=numpy.arange(1, 2, 0.2),
    #                                 sl_range=numpy.arange(0.5, 1, 0.1), strategy=strategy.BUY, strategy_name="numpy arrange")
    # strategy.strategy_optimizations(data_properties=data_prop, data_list=data, buy=buy,
    #                                 sell=[sell_1, sell_2], target_range=numpy.arange(0.5, 1.5, 0.2),
    #                                 sl_range=numpy.arange(0.5, 1.5, 0.2), strategy=strategy.BUY, strategy_name="list constants")

    output = []
    range_1 = [10,20,30,40,50]
    range_2 = [20,40,60,100,200]
    for i in range(len(range_1)):
        ema_1 = indicators.ema(close, period=range_1[i])
        ema_2 = indicators.ema(close, period=range_2[i])

        buy = Condition(data1=ema_1, data2=ema_2, operation=Operation.CROSSOVER)
        sell = Condition(data1=ema_1, data2=ema_2, operation=Operation.CROSSUNDER)

        result = strategy.strategy_builder(data_properties=data_prop, data_list=data, buy=buy, sell=sell,)
        output.append(result)

    strategy.eval_results(output, range_1=range_1, range_2=range_2)
