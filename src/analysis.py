from matplotlib import colors
import config, finnhub
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import mplfinance as mpf

def has_support(df, i):
    support = df['Low'][i] < df['Low'][i-1]  and df['Low'][i] < df['Low'][i+1] and df['Low'][i+1] < df['Low'][i+2] and df['Low'][i-1] < df['Low'][i-2]
    return support

def has_resistance(df, i):
    resistance = df['High'][i] > df['High'][i-1]  and df['High'][i] > df['High'][i+1] and df['High'][i+1] > df['High'][i+2] and df['High'][i-1] > df['High'][i-2]
    return resistance

def is_far(line, avg, levels):
    return np.sum([abs(line-x) < avg  for x in levels]) == 0

def support_resist(df):
    avg = np.mean(df['High'] - df['Low'])
    support = []
    resistance = []
    for i in range(2, df.shape[0]-2):
        if has_support(df, i):
            line = df['Low'][i]
            if is_far(line, avg, support):
                support.append(line)
        elif has_resistance(df, i):
            line = df['High'][i]
            if is_far(line, avg, resistance):
                resistance.append(line)
    return support, resistance


def get_candles(ticker, comp):
    current = datetime.now()
    end_timestamp = int(datetime.timestamp(current))
    past_yr = current - timedelta(weeks=52)
    start_stamp = int(datetime.timestamp(past_yr))
    
    finnhub_client = finnhub.Client(api_key=config.finnhub_key)
    res = finnhub_client.stock_candles(ticker, 'W', start_stamp, end_timestamp)
    
    
    df = pd.DataFrame.from_dict(res)
    ''' Adjusted for it being Sunday change when you get a chance '''
    current = datetime.now() - timedelta(5)
    end_timestamp = int(datetime.timestamp(current))
    past_yr = current - timedelta(weeks=len(df.index-1))
    start_stamp = int(datetime.timestamp(past_yr))
    dti = pd.date_range(start=str(datetime.fromtimestamp(start_stamp)), end=str(datetime.fromtimestamp(end_timestamp)), freq='W')
    
    df.columns = ['Close', 'High', 'Low', 'Open', 's', 't', 'Volume']
    ''' Keep volume '''
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
    df.index = dti
    print(df)
    support, resistance = support_resist(df)
    
    mpf.plot(df, type='candle', style='charles',
            hlines= dict(hlines=[support[-1], resistance[-1]], colors=['g', 'r'], linestyle='-.'), 
            title= str(ticker) + " - " + str(comp),
            ylabel= 'Price ($)',
            mav= 6,
            volume= True,
            savefig='./candle_docs/' + str(ticker) + '_candles.png')
    
    pattern_recognition(ticker, finnhub_client)
    
def pattern_recognition(ticker, finnhub_client):

    res = finnhub_client.pattern_recognition(ticker, 'W')
    if res:
        print(res['points'][0]['patternname'])
        print(res['points'][0]['patterntype'])    