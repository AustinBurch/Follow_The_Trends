import re, csv, time
import yfinance as yfi
from scrape_twitter import scrape_twitter
from scrape_reddit import scrape_reddit

def match_tickers(file, stock_dict):
    
    stock_failure = 0
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row[2]:
                match = re.findall('\$([A-Z]+)',row[2])
            else:
                match = re.findall('\$([A-Z]+)',row[1])
            if match: 
                i = 0
                while (i < len(match)):
                    try:
                        company = yfi.Ticker(match[i])
                        name = company.info['shortName']
                        stock_dict[match[i]] = name
                        time.sleep(2)
                        stock_failure = 0
                        i += 1
                    except ValueError:
                        print("Yahoo Finance Back-end Error, Attempting to Fix")  # An error occurred on Yahoo Finance's back-end. We will attempt to retreive the data again
                        if stock_failure > 5:  # Move on to the next ticker if the current ticker fails more than 5 times
                            i += 1
                        stock_failure += 1
    return stock_dict                  

if __name__ == '__main__':

    scrape_twitter()
    scrape_reddit()
    stock_dict = match_tickers('reddit_info.txt', {})
    print(stock_dict)
    stock_dict = match_tickers('twitter_info.txt', stock_dict)
    print(stock_dict)

