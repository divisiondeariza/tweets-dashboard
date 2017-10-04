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
            self._naive_destroy_tweet(tweet)
        except TweepError as e:    
            self._resolve_tweep_error(tweet, e)         
        finally:     
            tweet.save()
            
    def _resolve_tweep_error(self, tweet, e):
        if not e.api_code == 144:
            raise e
        else:
            tweet.exists_in_twitter = False
            
    def _naive_destroy_tweet(self, tweet):
        self.API.destroy_status(tweet.tweet_id)
        tweet.exists_in_twitter = False