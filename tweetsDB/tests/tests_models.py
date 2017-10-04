'''
Created on 4/10/2017

@author: emmanuel
'''
import unittest
from django.test.testcases import TestCase
from tweetsDB import models


class TestTweets(TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testRendersUrlCorrectly(self):
        tweet = models.Tweet.objects.create(tweet_id = "tweetid")
        self.assertEqual(tweet.url(), 
                         '<a target="_blank" href="https://twitter.com/statuses/tweetid">link to tweet</a>')
        
    def testIsResponseIsFalseWhenNoReplyStatusId(self):
        tweet = models.Tweet.objects.create(tweet_id = "tweetid")
        self.assertFalse(tweet.is_response())

    def testIsResponseIsTrueWhenReplyStatusId(self):
        tweet = models.Tweet.objects.create(tweet_id = "tweetid",
                                            in_reply_to_status_id = "anothertweetid")
        self.assertTrue(tweet.is_response())        
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()