import re, csv, time, requests, config, analysis
from scrape_twitter import scrape_twitter
from scrape_reddit import scrape_reddit

def match_tickers(file, stock_dict):
    
    stock_failure = 0
    with open(file) as csv_file:
        print("opening files")
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if file == 'reddit_info.txt':
                match = re.findall('\$([A-Z]+)',row[2])
            else:
                match = re.findall('\$([A-Z]+)',row[1])
                
            if match:
                i = 0
                while (i < len(match)):
                    
                    try:
                        search = 'https://finnhub.io/api/v1/search?q=' + match[i] + '&token=' + config.finnhub_key
                        r = requests.get(search)
                        info = r.json()
                        name = info['result'][0]['description']
                        stock_dict[match[i]] = name 
                        stock_failure = 0
                        i += 1
                    except ValueError:
                        print("FinnHub Back-end Error, Attempting to Fix")  # An error occurred on Finnhub's back-end. We will attempt to retreive the data again
                        if stock_failure > 3:  # Move on to the next ticker if the current ticker fails more than 3 times
                            i += 1
                        stock_failure += 1
                    time.sleep(1)    
    return stock_dict                           
    
if __name__ == '__main__':

    try:
        
        #scrape_twitter()
        #scrape_reddit()
        
        print("scrape successful")
        #stock_dict = match_tickers('reddit_info.txt', {})
        stock_dict = match_tickers('twitter_info.txt', {})
        if len(stock_dict) == 0:
            print("No tickers found")
        
        #time.sleep(60)
        #stock_dict = match_tickers('twitter_info.txt', stock_dict)
        
        for key, value in stock_dict.items():
            if key != 'DD' or key != 'YOLO':
                print(key)
                analysis.get_candles(key, value)
        
    except BaseException as e:
        print('failed scrape,', str(e))
