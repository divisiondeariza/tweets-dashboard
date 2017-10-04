'''
Created on 2/10/2017

@author: emmanuel
'''
import logger
from tweepy.error import TweepError

class Destroyer(object):

    def __init__(self):
        self.API = logger.login()

    
    def destroy(self, tweets_query):
        for tweet in tweets_query:
            self._destroy_tweet(tweet) 
    
    def _destroy_tweet(self, tweet):
        try: 
            self.API.destroy_status(tweet.tweet_id)
        except TweepError as e:    
            #print e
            pass
        finally:     
            tweet.exists_in_twitter = False
            tweet.save()