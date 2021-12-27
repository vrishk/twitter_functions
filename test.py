from datetime import datetime
from twitter_funcs import TwitterLoader
import pathlib
import argparse
import os
import boto3
from dateutil.parser import parse
import json
from dotenv import dotenv_values


def expand_path(string):
    if string:
        return pathlib.Path(os.path.expandvars(string))
    else:
        return None


def load_list(string, s3):
    assert string
    if not s3:
        loc = pathlib.Path(os.path.expandvars(string))
        assert loc.suffix == ".json"
        with open(loc, "r") as file:
            final_list = json.load(file)
    else:
        s3object = s3.Object("chainverse", string)
        final_list = s3object.get()["Body"].read().decode("utf-8")
        final_list = json.loads(final_list)

    return final_list


def str2bool(v):
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


def parse_date(s):
    if not s:
        return s
    try:
        ret = parse(s)
    except ValueError:
        ret = datetime.utcfromtimestamp(s)
    return ret


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--s3", type=str2bool, default=False, help="save output to s3")
    parser.add_argument("--since", type=parse_date, default=None, help="start date for which to query data")
    parser.add_argument("--until", type=parse_date, default=None, help="end time for which to query data")
    parser.add_argument("--input_path", type=str, required=True, help="where to load in input twitter handles")
    parser.add_argument("--output_path", type=str, required=True, help="where to save data")
    parser.add_argument("--top", type=int, default=10, help="number of top interacting accounts")
    flags = parser.parse_args()

    s3 = None
    if flags.s3:
        s3 = boto3.resource("s3")

    usernames = load_list(flags.input_path, s3)
    print(f"{len(usernames)} usernames loaded")

    config = dotenv_values(".env")
    tweepy_token = config["BEARER_TOKEN"]

    t = TwitterLoader(flags.output_path, flags.s3, tweepy_token, flags.since, flags.until)
    t.tweets(usernames)
    t.retweets(usernames)
    t.mentions(usernames)
    t.followers(usernames)
    t.following(usernames)
    t.topX_interactive(usernames, flags.top)

