import requests, csv, config, json, time
import pandas as pd
import mplfinance as fplt
from datetime import datetime, timedelta

def get_candles(ticker):

    
    current = datetime.now()
    end_timestamp = int(datetime.timestamp(current))
    past_yr = current - timedelta(weeks=52)
    start_stamp = int(datetime.timestamp(past_yr))
    
    r = requests.get('https://finnhub.io/api/v1/indicator?symbol=' + ticker + '&resolution=D&from=' + str(start_stamp) + '&to=' + str(end_timestamp) + '&token=' + config.finnhub_key)
    stock_info = r.json()
    df = pd.DataFrame.from_dict(stock_info, orient="index")
    df.to_csv("candle_docs/" + ticker + "_candles.csv")
    '''
    comp_file = open(ticker + "_candles.csv", 'w')
    csv_writer = csv.writer(comp_file)

    count = 0

    for points in stock_info:
        if count == 0:
            header = points.keys()
            csv_writer.writerow(header)
            count += 1
        csv_writer.writerow(points.values())
    comp_file.close()
        #candle_info = r.json()
        #candle_close = [candles['c'] for candles in candle_info]
        #print(key + " " + candle_close)
        #candles = json.loads(candle_info)
        #df = pd.json_normalize(candles['c'])
        #df.to_csv(r'' + value + '_candles.csv')
        '''