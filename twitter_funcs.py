import tweepy
import os

from typing import List

# Twitter API setup
from dotenv import load_dotenv
load_dotenv()

auth = tweepy.OAuthHandler(os.environ["API_KEY"], os.environ["API_SECRET_KEY"])
auth.set_access_token(os.environ["ACCESS_KEY"], os.environ["ACCESS_SECRET_KEY"])
api = tweepy.API(auth)

# Main class for loading twitter data

class TwitterLoader:
    def __init__(self, out_dir: str) -> None:
        self.out_dir = TwitterLoader.path(out_dir)

    @staticmethod
    def path(*path_slices: str):
        path = os.path.join(*path_slices)
        
        dir_path = os.path.dirname(path)
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)

        return path


    def tweets(
        self,
        unames: List[str], 
        since: str = None, 
        until: str = None
    ) -> None:

    
        all_tweets = []
        all_tweets.extend(tweets)
        oldest_id = tweets[-1].id
        while True:
            tweets = api.user_timeline(screen_name=userID, 
                                   # 200 is the maximum allowed count
                                   count=200,
                                   include_rts = False,
                                   max_id = oldest_id - 1,
                                   # Necessary to keep full_text 
                                   # otherwise only the first 140 words are extracted
                                   tweet_mode = 'extended'
                                   )
            if len(tweets) == 0:
                break
            oldest_id = tweets[-1].id
            all_tweets.extend(tweets)
            print('N of tweets downloaded till now {}'.format(len(all_tweets)))



