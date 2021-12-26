from datetime import datetime
from twitter_funcs import TwitterLoader


def main():
    t = TwitterLoader("outputs/test")
    t.tweets(["elonmusk"])
    t.retweets(["elonmusk"])
    t.mentions(["elonmusk"])

if __name__ == "__main__":
    main()
