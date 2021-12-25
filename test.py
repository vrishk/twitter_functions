from datetime import datetime
from twitter_funcs import TwitterLoader


def main():
    t = TwitterLoader("outputs/test")
    t.tweets(["elonmusk", "jack"], since="2021-12-23")
    t.retweets(["elonmusk", "jack"], since="2021-12-23")

if __name__ == "__main__":
    main()
