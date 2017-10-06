'''
Created on 2/10/2017

@author: emmanuel
'''
import csv
from tweetsDB import models
from django.db import transaction


class Loader(object):
    
    @transaction.atomic
    def load(self, filename):
        with open(filename,'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader: 
                self._create_tweet(row) 
    
    def _create_tweet(self, row):
        tweet, tweetWasCreated = models.Tweet.objects.get_or_create(tweet_id=row['tweet_id'])
        tweet.in_reply_to_status_id = row['in_reply_to_status_id']
        tweet.in_reply_to_user_id = row['in_reply_to_user_id']
        tweet.created_at = row['timestamp'].replace(" +", "+")
        tweet.source = row['source']
        tweet.text = row['text']
        tweet.retweeted_status_id = row['retweeted_status_id']
        tweet.retweeted_status_user_id = row['retweeted_status_user_id']
        if (row['retweeted_status_timestamp']):
            tweet.retweeted_status_timestamp = row['retweeted_status_timestamp'].replace(" +", "+")
        tweet.expanded_urls = row['expanded_urls']
        tweet.save()


