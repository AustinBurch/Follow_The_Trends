import praw, time, csv, re
import yfinance as yfi
import pandas as pd 


def scrape_reddit():
        try:
                reddit = praw.Reddit(client_id='id', client_secret='secret', user_agent='Folow_The_Trends')
                hot_posts = []
                for posts in reddit.subreddit('StockMarket').hot(limit=20):
                        hot_posts.append([posts.title,posts.selftext])
                for posts in reddit.subreddit('WallStreetBets').hot(limit=20):
                        hot_posts.append([posts.title,posts.selftext])
                posts = pd.DataFrame(hot_posts,columns=['title','selftext'])
                posts.to_csv(r'reddit_info.txt')
        except BaseException as e:
            print('failed on_status,', str(e))
            time.sleep(3)
       
