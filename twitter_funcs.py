import twint
import datetime
import os

from typing import List

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

        for uname in unames:
            c = twint.Config()

            c.Until = until
            c.Since = since

            c.Username = uname

            c.Store_json = True
            c.Filter_retweets = True
    
            c.Output = TwitterLoader.path(self.out_dir, uname, "tweets.json")

            twint.run.Search(c) 

    def retweets(
        self,
        unames: List[str], 
        since: str = None, 
        until: str = None
    ) -> None:

        for uname in unames:
            c = twint.Config()

            c.Until = until
            c.Since = since

            c.Username = uname

            c.Native_retweets = True
            c.Retweets = True

            c.Store_json = True
    
            c.Output = TwitterLoader.path(self.out_dir, uname, "retweets.json")

            twint.run.Search(c) 


    def mentions(
        self,
        unames: List[str], 
        since: str = None, 
        until: str = None
    ) -> None:

        for uname in unames:
            c = twint.Config()

            c.Until = until
            c.Since = since

            c.Username = uname

            c.Native_retweets = True
            c.Retweets = True

            c.Store_json = True
    
            c.Output = TwitterLoader.path(self.out_dir, uname, "retweets.json")

            twint.run.Search(c) 

    def followers(
        self,
        unames: List[str], 
    ) -> None:

        for uname in unames:
            c = twint.Config()

            c.Username = uname

            c.Native_retweets = True
            c.Retweets = True

            c.Store_json = True
    
            c.Output = TwitterLoader.path(self.out_dir, uname, "following.json")

            twint.run.Followers(c) 

    def followed(
        self,
        unames: List[str], 
    ) -> None:

        for uname in unames:
            c = twint.Config()

            c.Username = uname

            c.Native_retweets = True
            c.Retweets = True

            c.Store_json = True
    
            c.Output = TwitterLoader.path(self.out_dir, uname, "followed.json")

            twint.run.Following(c) 
