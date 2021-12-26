from datetime import datetime
from twitter_funcs import TwitterLoader


def main():
    t = TwitterLoader("outputs/test", since=datetime(2021, 12, 10))
    t.tweets(["elonmusk"])
    t.retweets(["elonmusk"])
    t.mentions(["elonmusk"])
    t.topX_interactive(["elonmusk"], 10)

if __name__ == "__main__":
    main()
