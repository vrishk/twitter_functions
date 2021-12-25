from datetime import datetime
from twitter_funcs import TwitterLoader


def main():
    t = TwitterLoader("outputs/test")
    t.followers([44196397])
    t.following([44196397])

if __name__ == "__main__":
    main()
