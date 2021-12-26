# Diamond DAO Twitter Functions

## Project Description

As Diamond DAO continues to grow out Chainverse and delve into some ML tasks, it is crucial that we have the ability to generate and analyze social media data pertaining to DAO's and contributors, especially on the Twitter front. Thus, we want to build out a set of functions (essentially a class) in Python that can be given a list of twitter handles (as well as potentially a set time frame) and create json documents with the following metrics:

- All tweets
- Get all retweets
- Get all mentions
- Find top X interacting handles (including those that comment, like, or frequently mention)
- Get all following account
- Get all followed accounts

## Project Setup

Install the `tweepy` (and `dotenv` dependency) and `snscrape` packages for scraping user data and unlimited tweets:

```{bash}
pip install tweepy python-dotenv, tqdm
pip install git+https://github.com/JustAnotherArchivist/snscrape.git
```

Note that `tweepy` requires a valid `BEARER_TOKEN` by signing up at dev.twitter.com.


## Usage

The main class is the `TwitterLoader` in the `twitter_functions.py` file. All the functions with their usage is provided in the same file.

For example, to mine all tweets from @elonmusk:

```
t = TwitterLoader("outputs/elon", since=datetime(2021, 12, 10))
t.tweets(["elonmusk"])
```
