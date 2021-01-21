import tweepy, time, re, csv
import yfinance as yfi
import pandas as pd

def scrape_twitter():

    consumer_key = "consumer"
    consumer_secret = "secret"
    access_token = "token"
    access_token_secret = "token_secret"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth,wait_on_rate_limit=True)

    text_query = '#StocksToWatch'
    max_tweets = 50


    try:
            # Creation of query method using parameters
            tweets = tweepy.Cursor(api.search,q=text_query, count=50, result_type='recent', lang="en").items(max_tweets)

            # Pulling information from tweets iterable object
            tweets_list = [[ tweet.text] for tweet in tweets]

            # Creation of dataframe from tweets list
            # Add or remove columns as you remove tweet info
            tweets_df = pd.DataFrame(tweets_list)
            tweets_df.to_csv(r'twitter_info.txt')

    except BaseException as e:
            print('failed on_status,', str(e))
            time.sleep(3)
    
   
