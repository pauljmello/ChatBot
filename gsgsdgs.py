from alpha_vantage.timeseries import TimeSeries
import pandas as pd

def get_ticker_info_adjusted_daily_total(ticker):
    TS = TimeSeries(key='YJH452CREZ8Z0DC0', output_format='pandas')
    data = TS.get_daily_adjusted(ticker, outputsize='compact')
    data = data[0]
    data = pd.DataFrame(data)
    print(data)
    return(data)

get_ticker_info_adjusted_daily_total("AAPL")