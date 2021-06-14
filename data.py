import pandas as pd
import pandas_datareader.data as pdr
from datetime import datetime
# api's for stock data
from alpha_vantage.timeseries import TimeSeries
import yfinance as yf


def stock_data(ticker):
    end = datetime.now()
    start = datetime(end.year-2,end.month,end.day)
    data = yf.download(ticker, start=start, end=end)
    df = pd.DataFrame(data=data)
    df.to_csv(''+ticker+'.csv')
    if(df.empty):
        ts = TimeSeries(key='N6A6QT6IBFJOPJ70',output_format='pandas')
        data, meta_data = ts.get_daily_adjusted(symbol='NSE:'+ticker, outputsize='full')
        #Format df
        #Last 2 yrs rows => 502, in ascending order => ::-1
        data=data.head(503).iloc[::-1]
        data=data.reset_index()
        #Keep Required cols only
        df=pd.DataFrame()
        df['Date']=data['date']
        df['Open']=data['1. open']
        df['High']=data['2. high']
        df['Low']=data['3. low']
        df['Close']=data['4. close']
        df['Adj Close']=data['5. adjusted close']
        df['Volume']=data['6. volume']
        df.to_csv(''+ticker+'.csv',index=False)
    return