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

Install the required packages from the requirements.txt file:

```{bash}
pip install -r requirements.txt
```

Note that `tweepy` requires a valid `BEARER_TOKEN` by signing up at dev.twitter.com.
Additionally, ensure you have s3 access keys in your environment or in the proper .aws directory.

## Usage

The main class is the `TwitterLoader` in the `twitter_functions.py` file. All the functions with their usage is provided in the same file.

