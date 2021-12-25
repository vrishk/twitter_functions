import tweepy
import os
import json

from typing import List, Dict

# Twitter API setup
from dotenv import load_dotenv
load_dotenv()

client = tweepy.Client(bearer_token=os.environ["BEARER_TOKEN"])

# Constants

MAX_NUM_TWEETS = 20

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

    def save(self, data: Dict, kind: str):
        path = TwitterLoader.path(self.out_dir, kind + ".json")
        with open(path, "w+") as f:
            json.dump(data, f)

    def load(self, kind: str):
        path = TwitterLoader.path(self.out_dir, kind + ".json")
        print(path)
        with open(path, "r") as f:
            return json.load(f)
    

    def tweets(
        self,
        uids: List[int], 
    ) -> None:
        
        tweet_fields = ['id', 'text', 'in_reply_to_user_id']
        tweets = {}
        for uid in uids:    
            user_tweets =  tweepy.Paginator(
                client.get_users_tweets, id=uid, tweet_fields=tweet_fields, max_results=10, exclude="retweets"
            ).flatten(limit=MAX_NUM_TWEETS)

            tweets[uid] = [
                {key: tweet[key] for key in tweet_fields} 
                for tweet in user_tweets if "RT @" not in tweet.text
            ]

        self.save(tweets, "tweets")

    def retweets(
        self,
        uids: List[int], 
    ) -> None:
        
        tweet_fields = ['id', 'text', 'in_reply_to_user_id']
        tweets = {}
        for uid in uids:    
            user_tweets =  tweepy.Paginator(
                client.get_users_tweets, id=uid, tweet_fields=tweet_fields, max_results=10
            ).flatten(limit=MAX_NUM_TWEETS)
            
            tweets[uid] = [
                {key: tweet[key] for key in tweet_fields} 
                for tweet in user_tweets if "RT @" in tweet.text
            ]

        self.save(tweets, "retweets")

    def mentions(
        self,
        uids: List[int], 
        since: str = None,
        until: str = None,
    ) -> None:
        
        tweet_fields = ['id', 'text', 'in_reply_to_user_id']
        tweets = {}
        for uid in uids:    
            user_tweets =  tweepy.Paginator(
                client.get_users_mentions,
                id=uid, tweet_fields=tweet_fields, 
                start_time=since, end_time=until,
                max_results=10
            ).flatten(limit=MAX_NUM_TWEETS)
            
            tweets[uid] = [
                {key: tweet[key] for key in tweet_fields} 
                for tweet in user_tweets
            ]

        self.save(tweets, "mentions")


    def followers(self, uids: List[int]) -> None:

        followers = {}
        for uid in uids:    
            users = client.get_users_followers(id=uid).data
            followers[uid] = [{"id": user.id, "username": user.username} for user in users]

        self.save(followers, "followers")

    def following(self, uids: List[int]) -> None:

        following = {}
        for uid in uids:    
            users = client.get_users_following(id=uid).data
            following[uid] = [{"id": user.id, "username": user.username} for user in users]

        self.save(following, "following")

