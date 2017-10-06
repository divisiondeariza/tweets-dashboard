'''
Created on 4/10/2017

@author: emmanuel
'''
from libs.twitter_utils import logger
import tweepy
from tweetsDB import models

class TimelineSaver(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.API = logger.login()

    def save(self):
        for status in tweepy.Cursor(self.API.user_timeline).items():
            tweet, wasCreated = models.Tweet.objects.get_or_create(tweet_id = status.id)
            tweet.in_reply_to_status_id = status.in_reply_to_status_id
            tweet.in_reply_to_user_id = status.in_reply_to_user_id
            tweet.created_at = status.created_at.strftime("%Y-%m-%d %H:%M:%S+0000")
            tweet.source = status.source
            tweet.text = status.text
            tweet.retweets_count = status.retweet_count
            tweet.likes_count = status.favorite_count                                                        

            if status.retweeted:
                tweet.retweeted_status_id = status.retweeted_status.id
                tweet.retweeted_status_user_id = status.retweeted_status.author.id
                tweet.retweeted_status_created_at = status.retweeted_status.created_at.strftime("%Y-%m-%d %H:%M:%S+0000")
            tweet.save()
             
                                                                    

        



