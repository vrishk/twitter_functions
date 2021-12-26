import tweepy
import snscrape.modules.twitter as sntwitter
import collections
import itertools 
import os
import json

from datetime import datetime
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
    def __init__(self, out_dir: str, since: datetime = None, until: datetime = None) -> None:
        """Init function for Twitter data loader

        Args:
            out_dir: path to output directory
            since: datetime object from when data is collected. Default 
                is earliest time when data is available. Only date-level precision.
            until: datetime object till when data is collected. Default 
                is present date. Only date-level precision.
        """
        self.out_dir = TwitterLoader.path(out_dir)
        
        format = "%Y-%m-%d"
        self.interval_str = ""
        if until is not None:
            self.interval_str += f" until:{until.strftime(format)}"
        if since is not None:
            self.interval_str += f" since:{since.strftime(format)}"

    @staticmethod
    def path(*path_slices: str):
        """Safe path creation and access function"""
        path = os.path.join(*path_slices)
        
        dir_path = os.path.dirname(path)
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)

        return path

    def save(self, data: Dict, kind: str):
        """Save dictionary data as json in output_dir"""
        path = TwitterLoader.path(self.out_dir, kind + ".json")
        with open(path, "w+") as f:
            json.dump(data, f)

    def load(self, kind: str):
        """Load json data from output_dir"""
        path = TwitterLoader.path(self.out_dir, kind + ".json")
        with open(path, "r") as f:
            return json.load(f)

    def scrape(self, query: str, filter_retweets: str = "include") -> List[Dict]:
        """Scrape data corresponding to a query

        Args:
            query: The search query to obtain tweets. Example format 'from:username'.
            filter_retweets: Filtering retweets - 'only' (only retweets), 'include' 
                (tweets and retweets), 'exclude' (no retweets)
        Returns:
            List of tweet dictionaries with tweet id, username of tweet, content (text),
            date and time of tweet, username replied to (if it is a reply tweet), 
            mentioned users (@user mentions if any)
        """

        query += self.interval_str
        user_tweets = sntwitter.TwitterSearchScraper(query).get_items()

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
                "username": raw_tweet.user.username,
                "content": raw_tweet.content, 
                "date": str(raw_tweet.date),
                "reply_to": None if raw_tweet.inReplyToUser is None else raw_tweet.inReplyToUser.username,
                "mentioned_users": [] if raw_tweet.mentionedUsers is None else [user.username for user in raw_tweet.mentionedUsers]
            })

            # Ensure that number of tweets are limited
            if i >= MAX_NUM_TWEETS:
                break

        return tweet

    def tweets(
        self,
        usernames: List[str], 
    ) -> None:
        """Scrape all tweets (excluding retweets) from a list of usernames and store in output_dir/tweets.json"""
        
        tweets = {}

        for uname in usernames:
            tweets[uname] = self.scrape(f"from:{uname}", filter_retweets="exclude")

        self.save(tweets, "tweets")

    def retweets(
        self,
        usernames: List[str], 
    ) -> None:
        """Scrape all retweets from a list of usernames and store in output_dir/retweets.json"""
        
        tweets = {}
        for uname in usernames:
            tweets[uname] = self.scrape(f"from:{uname} include:nativeretweets", filter_retweets="only")

        self.save(tweets, "retweets")

    def mentions(
        self,
        usernames: List[str], 
    ) -> None:
        """Scrape all tweets with mentions of usernames in the list and store in output_dir/mentions.json"""
                
        tweets = {}
        for uname in usernames:
            tweets[uname] = self.scrape(f"@{uname}", filter_retweets="exclude")
    
        self.save(tweets, "mentions")
    
    def topX_interactive(self, usernames: List[str], X: int):
        """Find top-X interactive users with a given list of users and store in output_dir/top_interactive.json

        Creates lists of top-X interactive users by the following criteria:
            - Mentions by a given user
            - Mentions of a given user
            - Replies from a given user

        Note: this requires that the TwitterLoader.tweets() and TwitterLoader.mentions()
            be run on the same set of usernames as it uses that data.
        """
        
        tweets = self.load("tweets")
        mentions = self.load("mentions")

        def get_topX(unames: List[str], _X: int) -> List[str]:
            freq_list = collections.Counter(unames).items()
            freq_list = sorted(freq_list, key=lambda pair: -pair[1])[:_X]

            return [pair[0] for pair in freq_list]


        top_interactive = {}

        for uname in usernames:

            top_interactive[uname] = {}

            main_user_mentions = list(itertools.chain(*[tweet["mentioned_users"] for tweet in tweets[uname]]))
            top_interactive[uname]["main_user_mentions"] = get_topX(main_user_mentions, X)

            other_user_mentions = [tweet["username"] for tweet in mentions[uname]]
            top_interactive[uname]["other_user_mentions"] = get_topX(other_user_mentions, X)

            replies_to_users = [tweet["reply_to"] for tweet in tweets[uname] if tweet["reply_to"] is not None]
            top_interactive[uname]["replies_to_users"] = get_topX(replies_to_users, X)

        self.save(top_interactive, "top_interactive")
        

    def followers(self, usernames: List[str]) -> None:
        """Scrape all followers from a list of usernames and store in output_dir/followed.json"""

        followers = {}
        for uname in usernames:    
            uid = client.get_user(username=uname).data.id
            users = client.get_users_followers(id=uid).data
            followers[uid] = [{"id": user.id, "username": user.username} for user in users]

        self.save(followers, "followers")

    def following(self, usernames: List[str]) -> None:
        """Scrape users followed by a list of usernames and store in output_dir/following.json"""

        following = {}
        for uname in usernames:    
            uid = client.get_user(username=uname).data.id
            users = client.get_users_following(id=uid).data
            following[uid] = [{"id": user.id, "username": user.username} for user in users]

        self.save(following, "following")

