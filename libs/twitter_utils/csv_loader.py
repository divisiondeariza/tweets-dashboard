'''
Created on 2/10/2017

@author: emmanuel
'''
import csv
from tweetsDB import models
from django.db import transaction


FIELD_ALIASES = {
    'tweet_id': ['tweet_id', 'id', 'tweetId', 'tweet.id'],
    'in_reply_to_status_id': ['in_reply_to_status_id', 'inReplyToTweetId', 'reply_to_tweet_id'],
    'in_reply_to_user_id': ['in_reply_to_user_id', 'inReplyToUserId', 'reply_to_user_id'],
    'timestamp': ['timestamp', 'created_at', 'createdAt', 'date', 'tweet_created_at'],
    'source': ['source', 'sourceLabel', 'source_label'],
    'text': ['text', 'content', 'renderedContent', 'full_text', 'tweet', 'cleaned_tweet'],
    'retweeted_status_id': ['retweeted_status_id', 'retweetedTweet.id', 'retweeted_tweet_id'],
    'retweeted_status_user_id': ['retweeted_status_user_id', 'retweetedTweet.user.id', 'retweeted_user_id'],
    'retweeted_status_timestamp': ['retweeted_status_timestamp', 'retweetedTweet.date', 'retweeted_created_at'],
    'expanded_urls': ['expanded_urls', 'outlinks', 'url', 'tweet_url'],
    'likes_count': ['likes_count', 'likeCount', 'favorite_count'],
    'retweets_count': ['retweets_count', 'retweetCount', 'retweet_count'],
}


def _row_value(row, field_name, default=''):
    for alias in FIELD_ALIASES[field_name]:
        value = row.get(alias)
        if value not in (None, ''):
            return value
    return default


def _normalize_timestamp(value):
    if not value:
        return ''
    return value.replace(" +", "+")


class Loader(object):
    
    @transaction.atomic
    def load(self, filename):
        with open(filename,'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader: 
                self._create_tweet(row) 
    
    def _create_tweet(self, row):
        tweet_id = _row_value(row, 'tweet_id')
        if not tweet_id:
            raise ValueError('CSV row is missing tweet_id, id, or tweetId.')

        tweet, tweetWasCreated = models.Tweet.objects.get_or_create(tweet_id=tweet_id)
        tweet.in_reply_to_status_id = _row_value(row, 'in_reply_to_status_id')
        tweet.in_reply_to_user_id = _row_value(row, 'in_reply_to_user_id')
        tweet.created_at = _normalize_timestamp(_row_value(row, 'timestamp'))
        tweet.source = _row_value(row, 'source', 'CSV import')
        tweet.text = _row_value(row, 'text')
        tweet.retweeted_status_id = _row_value(row, 'retweeted_status_id')
        tweet.retweeted_status_user_id = _row_value(row, 'retweeted_status_user_id')
        retweeted_timestamp = _row_value(row, 'retweeted_status_timestamp')
        if (retweeted_timestamp):
            tweet.retweeted_status_created_at = _normalize_timestamp(retweeted_timestamp)
        tweet.expanded_urls = _row_value(row, 'expanded_urls')
        tweet.likes_count = _row_value(row, 'likes_count') or None
        tweet.retweets_count = _row_value(row, 'retweets_count') or None
        tweet.save()

