import tweepy
import os
import json

from typing import List, Dict

# Twitter API setup
from dotenv import load_dotenv
load_dotenv()

client = tweepy.Client(bearer_token=os.environ["BEARER_TOKEN"])

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
    

    def tweets(
        self,
        uids: List[int], 
        since: str = None, 
        until: str = None
    ) -> None:
        
        pass

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





