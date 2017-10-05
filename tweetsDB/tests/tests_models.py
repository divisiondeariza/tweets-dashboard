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
        
    def testGetRatingMean(self):
        rating1 = models.Rating.objects.create(name = "rating1", weight = 0.1)
        rating2 = models.Rating.objects.create(name = "rating2", weight = 0.3)
        tweet = models.Tweet.objects.create(tweet_id = "tweetid",
                                            in_reply_to_status_id = "anothertweetid")
        rating_score1 = models.RatingScore.objects.create(tweet = tweet,
                                                  group = rating1,
                                                  score = 10)
        rating_score2 = models.RatingScore.objects.create(tweet = tweet,
                                                  group = rating2,
                                                  score = 5)        
        self.assertEqual(tweet.mean_rating(), 6.25)
    
    def testRatingIsZeroWhenSumOfWeightsIsZero(self):
        rating1 = models.Rating.objects.create(name = "rating1", weight = 0)
        rating2 = models.Rating.objects.create(name = "rating2", weight = 0)
        tweet = models.Tweet.objects.create(tweet_id = "tweetid",
                                            in_reply_to_status_id = "anothertweetid")
        rating_score1 = models.RatingScore.objects.create(tweet = tweet,
                                                  group = rating1,
                                                  score = 10)
        rating_score2 = models.RatingScore.objects.create(tweet = tweet,
                                                  group = rating2,
                                                  score = 5)        
        self.assertEqual(tweet.mean_rating(), 0)        
   
class TestRating(TestCase):
    
    def testUnicodeIsSetCorrectly(self):
        rating = models.Rating.objects.create(name = "a rating" , weight = 0.5)
        self.assertEqual(str(rating), "{0} ({1})".format(rating.name, rating.weight))
    
    def testWeightIsOneByDefault(self):
        rating = models.Rating.objects.create(name = "a rating")
        self.assertEqual(rating.weight, 1)
     
    def testWeightcanotBeGreaterThanOne(self):
        with self.assertRaises(ValidationError):
            rating = models.Rating.objects.create(name = "a rating", weight = 1.1)
            rating.full_clean()
 
    def testWeightcanotBeLessThanZero(self):
        with self.assertRaises(ValidationError):
            rating = models.Rating.objects.create(name = "a rating", weight = -0.1)
            rating.full_clean()   
            
        
class TestRatingScore(TestCase):

    def setUp(self):
        self.tweet = models.Tweet.objects.create(tweet_id = "tweetid")
        self.group = models.Rating.objects.create(name = "a group")


    def tearDown(self):
        pass

    def testScoreCannotBeGreaterThan10(self):
        with self.assertRaises(ValidationError):
            rating_score = models.RatingScore.objects.create(tweet = self.tweet,
                                                  group = self.group,
                                                  score = 11)
            rating_score.full_clean()
        
    def testScoreCannotBeLessThanZero(self):
        with self.assertRaises(ValidationError):
            rating = models.RatingScore.objects.create(tweet = self.tweet,
                                                  group = self.group,
                                                  score = -1)
            rating.full_clean()          
            
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()