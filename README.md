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

Install the `twint` package for scraping tweets:

```{bash}
$ pip install --upgrade git+https://github.com/himanshudabas/twint.git@origin/master#egg=twint
```


all_tweets = []
all_tweets.extend(tweets)
oldest_id = tweets[-1].id
while True:
    tweets = api.user_timeline(screen_name=userID, 
                           # 200 is the maximum allowed count
                           count=200,
                           include_rts = False,
                           max_id = oldest_id - 1,
                           # Necessary to keep full_text 
                           # otherwise only the first 140 words are extracted
                           tweet_mode = 'extended'
                           )
    if len(tweets) == 0:
        break
    oldest_id = tweets[-1].id
    all_tweets.extend(tweets)
    print('N of tweets downloaded till now {}'.format(len(all_tweets)))

