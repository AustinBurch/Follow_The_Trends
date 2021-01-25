import tweepy, time
import pandas as pd
import config

def scrape_twitter():

        auth = tweepy.OAuthHandler(config.twitter_consumer, config.twitter_secret)
        auth.set_access_token(config.twitter_token, config.twitter_token_secret)
        api = tweepy.API(auth,wait_on_rate_limit=True)

        text_query = '#StocksToWatch'
        max_tweets = 25


        try:
                # Creation of query method using parameters
                tweets = tweepy.Cursor(api.search,q=text_query, count=25, result_type='recent', lang="en").items(max_tweets)

                # Pulling information from tweets iterable object
                tweets_list = [[tweet.text] for tweet in tweets]

                # Creation of dataframe from tweets list
                # Add or remove columns as you remove tweet info
                tweets_df = pd.DataFrame(tweets_list)
                tweets_df.to_csv(r'twitter_info.txt')

        except BaseException as e:
                print('failed twitter scrape,', str(e))
                time.sleep(3)


