from twitter_funcs import TwitterLoader


def main():
    t = TwitterLoader("outputs/test")
    t.all_tweets(["jack", "elonmusk"])

if __name__ == "__main__":
    main()
