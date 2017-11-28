import tweepy
from secrets import *
import requests
import re
from random import choice, randint

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

cached_tweets = {}


def get_tweets(user_name):
    """Retrieves last 200 user tweets via tweepy API. Removes retweets, links,
    filters out unicode and saves to file"""
    user_tweets = api.user_timeline(screen_name=user_name, count=200)

    with open('tweets.txt', 'w') as f:
        for tweets in user_tweets:
            if (not tweets.retweeted and '@' not in tweets.text):
                #sub links in tweets with spaces
                user_tweets = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', tweets.text)
                #sub hashtags and misc punctuation in tweets with spaces
                # user_tweets = re.sub(r'(\#|\.|\-|\:|\'|\!|\?|\`|\/|\)|\(|\=|\_|\&|\%|\"|\,|\;|\~)', '', user_tweets)
                user_tweets = re.sub(r'(\#)', '', user_tweets)
                #filter everything except letters and spaces
                regex_filter = re.compile(r'^([a-zA-z\s]*)$')
                filtered_tweets = filter(regex_filter.search, user_tweets)
                #save user tweets to a text file
                f.write(filtered_tweets)
                f.write('\r\n')
    return


def open_and_read_file(file_path):
    """Take file path as string; return text as string.
    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """
    with open(file_path) as f:
        text = f.read()
    return text


def make_chains(text_string):
    """Take input text as string; return dictionary of Markov chains.
    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.
    For example:
        >>> chains = make_chains("hi there mary hi there juanita")
    Each bigram (except the last) will be a key in chains:
        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]
    Each item in chains is a list of all possible following words:
        >>> chains[('hi', 'there')]
        ['mary', 'juanita']
        >>> chains[('there','juanita')]
        [None]
    """
    words = text_string.split()
    chains = {}

    for i in range(len(words)-2):
        key = (words[i], words[i + 1])
        value = words[(i + 2)]

        if key not in chains:
            chains[key] = [value]
        else:
            chains[key].append(value)


    return chains

def create_tweet(chains):
    """Takes dictionary of markov chains; returns random text."""
    #generate random tweet length under 140 characters
    max_length = randint(1, 140)

    key = choice(chains.keys())
    words = [key[0], key[1]]
    while key in chains:
        # Keep looping until we have a key that isn't in the chains
        word = choice(chains[key])
        chain_length = len(" ".join(words))
        if chain_length > max_length:
            break
        words.append(word)
        key = (key[1], word)
    tweet = " ".join(words)
    tweet = tweet.capitalize()
    return tweet


def generate_user_tweets(username):
    """call all functions and generate tweet if user is not in cached tweets,
    otherwise same tweet is displayed"""
    if username not in cached_tweets:
        file_path = "tweets.txt"
        get_tweets(username)
        user_tweets = open_and_read_file(file_path)
        tweet_chains = make_chains(user_tweets)
        tweets = create_tweet(tweet_chains)
        # save user tweets in dictionary for quicker load on page
        cached_tweets[username] = tweets
    return cached_tweets[username]
