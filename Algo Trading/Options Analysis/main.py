from datetime import date

import option_strategy as opt

if __name__ == '__main__':
    # TODO: Begin from here
    # TODO: 1. Define some info
    symbol = 'nifty'
    expiry_month = 10
    expiry_year = 2018
    start_strike = 9500
    end_strike = 11500
    gap = 100
    start_date = date(2018, 9, 27)
    last_date = date(2018, 10, 20)
    timestamp = date(2018, 10, 23)
    # TODO: 2. Max Pain Analysis
    # opt.max_pain(symbol, expiry_month, expiry_year, timestamp=timestamp)
    # opt.max_pain(symbol, expiry_month, expiry_year, start_strike, end_strike, gap=gap, timestamp=timestamp)
    opt.max_pain(symbol, expiry_month, expiry_year, start_strike=start_strike, end_strike=end_strike, gap=gap)
    # opt.max_pain(symbol, expiry_month, expiry_year, start_strike, end_strike, gap=gap, start_date=start_date,
    #              last_date=last_date, )
