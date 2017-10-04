'''
Created on 4/10/2017

@author: emmanuel
'''
import unittest
from django.test.testcases import TestCase
from tweetsDB import models
from django.core.exceptions import ValidationError
from unittest.case import skip


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
   
class TestRatingGroup(TestCase):
    
    def testWeightIsOneByDefault(self):
        group = models.Rating.objects.create(name = "a group")
        self.assertEqual(group.weight, 1)
     
    def testWeightcanotBeGreaterThanOne(self):
        with self.assertRaises(ValidationError):
            group = models.Rating.objects.create(name = "a group", weight = 1.1)
            group.full_clean()
 
    def testWeightcanotBeLessThanZero(self):
        with self.assertRaises(ValidationError):
            group = models.Rating.objects.create(name = "a group", weight = -0.1)
            group.full_clean()   
        
class TestRating(TestCase):

    def setUp(self):
        self.tweet = models.Tweet.objects.create(tweet_id = "tweetid")
        self.group = models.Rating.objects.create(name = "a group")


    def tearDown(self):
        pass

    def testScoreCannotBeGreaterThan10(self):
        with self.assertRaises(ValidationError):
            rating = models.RatingScore.objects.create(tweet = self.tweet,
                                                  group = self.group,
                                                  score = 11)
            rating.full_clean()
        
    def testScoreCannotBeLessThanZero(self):
        with self.assertRaises(ValidationError):
            rating = models.RatingScore.objects.create(tweet = self.tweet,
                                                  group = self.group,
                                                  score = -1)
            rating.full_clean()          
            
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()