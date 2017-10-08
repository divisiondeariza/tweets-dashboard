'''
Created on 7/10/2017

@author: emmanuel
'''
import unittest
from tweetsDB import models, adminfilters
from tweetsDB.models import Tweet
from tweetsDB.admin import TweetAdmin
from django.test.testcases import TestCase


class TestIsResponseFilter(TestCase):

    def setUp(self):
        models.Tweet.objects.create(tweet_id = "response1",
                                    created_at = "2017-09-25 13:41:10+0000",
                                    in_reply_to_user_id = 'userid')
        models.Tweet.objects.create(tweet_id = "response2",
                                    created_at = "2017-09-25 13:41:10+0000",
                                    in_reply_to_status_id = 'statusid')
        models.Tweet.objects.create(tweet_id = "no-response1",
                                    created_at = "2017-09-25 13:41:10+0000",
                                    in_reply_to_user_id = None,
                                    in_reply_to_status_id = '')



    def tearDown(self):
        pass


    def testGetResponseTweetsCorrectly(self):
        filter = adminfilters.IsResponseFilter(None, {'is_response': "yes"}, Tweet, TweetAdmin)
        tweets = filter.queryset(None, Tweet.objects.all())
        self.assertListEqual(['response1', 'response2'], [tweet.tweet_id for tweet in tweets])

    def testGetNotResponseTweetsCorrectly(self):
        filter = adminfilters.IsResponseFilter(None, {'is_response': "no"}, Tweet, TweetAdmin)
        tweets = filter.queryset(None, Tweet.objects.all())
        self.assertListEqual(['no-response1'], [tweet.tweet_id for tweet in tweets])

class TestIsRetweetFilter(TestCase):
    def setUp(self):
        models.Tweet.objects.create(tweet_id = "retweet",
                                    created_at = "2017-09-25 13:41:10+0000",
                                    retweeted_status_id = 'statusid')
        models.Tweet.objects.create(tweet_id = "no-retweet1",
                                    created_at = "2017-09-25 13:41:10+0000",
                                    retweeted_status_id = '')
        models.Tweet.objects.create(tweet_id = "no-retweet2",
                                    created_at = "2017-09-25 13:41:10+0000",
                                    retweeted_status_id = None)

    def testGetRetweetsCorrectly(self):
        filter = adminfilters.IsRetweetFilter(None, {'is_retweet': "yes"}, Tweet, TweetAdmin)
        response_tweets = filter.queryset(None, Tweet.objects.all())
        self.assertListEqual(['retweet'], [tweet.tweet_id for tweet in response_tweets])
    
    def testGetNonRetweetsCorrectly(self):
        filter = adminfilters.IsRetweetFilter(None, {'is_retweet': "no"}, Tweet, TweetAdmin)
        response_tweets = filter.queryset(None, Tweet.objects.all())
        self.assertListEqual(['no-retweet1','no-retweet2'], [tweet.tweet_id for tweet in response_tweets])   
    