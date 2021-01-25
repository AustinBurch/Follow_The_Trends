import praw, time, config
import pandas as pd 


def scrape_reddit():
        try:
                reddit = praw.Reddit(client_id=config.reddit_id, client_secret=config.reddit_secret, user_agent='Folow_The_Trends')
                hot_posts = []
                for posts in reddit.subreddit('StockMarket').hot(limit=5):
                        hot_posts.append([posts.title,posts.selftext])
                for posts in reddit.subreddit('WallStreetBets').hot(limit=5):
                        hot_posts.append([posts.title,posts.selftext])
                posts = pd.DataFrame(hot_posts,columns=['title','selftext'])
                posts.to_csv(r'reddit_info.txt')
        except BaseException as e:
                print('failed reddit scrape,', str(e))
                time.sleep(3)

