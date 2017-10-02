'''
Created on 1/10/2017

@author: emmanuel
'''

import tweepy
from libs.twitter_utils.secrets import consumer_key, consumer_secret, access_token, access_token_secret

def login():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)

