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

    def all_tweets(
        self,
        unames: List[str], 
        since: datetime.datetime = None, 
        until: datetime.datetime = None
    ) -> None:

        since_str = since.strftime("%x").replace("/", "-") if since else None

        until_str = until.strftime("%x").replace("/", "-") if until else None

        for uname in unames:
            c = twint.Config()

            c.Until = until_str
            c.Since = since_str

            c.Username = uname

            c.Store_json = True
            c.Filter_retweets = True
    
            c.Output = TwitterLoader.path(self.out_dir, uname, "all.json")

            twint.run.Search(c) 
