import tweepy
import snscrape.modules.twitter as sntwitter
import datetime
import os
import json

from tqdm import tqdm

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

    @staticmethod
    def scrape(query: str, filter_retweets: str = "include") -> List[Dict]:
        user_tweets = sntwitter.TwitterSearchScraper(query + " since:2021-12-10").get_items()

        tweet = []

        print(f"Scraping query `{query}`...")
        for i, raw_tweet in tqdm(enumerate(user_tweets), total=MAX_NUM_TWEETS):
            # If only retweets required
            if filter_retweets == "only" and "RT @" not in raw_tweet.content:
                continue
            # If retweets need to be removed
            elif filter_retweets == "exclude" and "RT @" in raw_tweet.content:
                continue

            tweet.append({
                "id": raw_tweet.id, 
                "content": raw_tweet.content, 
                "date": str(raw_tweet.date)})

            # Ensure that number of tweets are limited
            if i >= MAX_NUM_TWEETS:
                break

        return tweet

    def tweets(
        self,
        usernames: List[str], 
    ) -> None:
        
        tweets = {}
        print("Extract tweets...")
        for uname in usernames:    
            tweets[uname] = TwitterLoader.scrape(f"from:{uname}", filter_retweets="exclude")

        self.save(tweets, "tweets")

    def retweets(
        self,
        usernames: List[str], 
    ) -> None:
        
        tweets = {}
        for uname in usernames:    
            tweets[uname] = TwitterLoader.scrape(f"from:{uname} include:nativeretweets", filter_retweets="only")

        self.save(tweets, "retweets")

    def mentions(
        self,
        usernames: List[str], 
        since: str = None,
        until: str = None,
    ) -> None:
                
        tweets = {}
        for uname in usernames:    
            tweets[uname] = TwitterLoader.scrape(f"@{uname}", filter_retweets="exclude")
    
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

