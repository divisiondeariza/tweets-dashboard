'''
Created on 1/10/2017

@author: emmanuel
'''
import unittest
from tweetsDB import models
from .. import tweets_scrapper 
from unittest.case import skip
from mock.mock import patch, Mock
from django.test.testcases import TestCase

class Status_mock():
    def __init__(self, id, retweets, likes):
        self.id = id
        self.text = "some text from {0}".format(id)
        self.retweet_count = retweets
        self.favorite_count = likes 

class TestTweetsScrapper(unittest.TestCase):


    def setUp(self):
        for i in range(200):
            tweet, tweetWasCreated = models.Tweet.objects.get_or_create(tweet_id = "dummyid{0}".format(i),
                                                                        timestamp = "2017-09-25 13:41:10+0000")


    def tearDown(self):
        pass

    @skip("")
    def testTweets(self):
        pass
    
    
class TestChunkSaver(TestCase):


    def setUp(self):
        for i in range(2):
            tweet = models.Tweet.objects.create(tweet_id = "id{0}".format(i),
                                                timestamp = "2017-09-25 13:41:10+0000")
            
        self.mock_API = Mock()
        self.mock_API.statuses_lookup = Mock(return_value = [Status_mock('id0', 0, 1),
                                                                   Status_mock('id1', 2, 3)])
    def tearDown(self):
        pass


    @patch(__name__ + '.tweets_scrapper.logger')
    def testSaveCallsAPIForDataCorrectly(self, mock_logger):
        mock_logger.login = Mock(return_value = self.mock_API)
        chunkSaver = tweets_scrapper.ChunkSaver()
        chunkSaver.save(['id1','id2'])
        self.mock_API.statuses_lookup.assert_called_once_with(['id1','id2'])

    @patch(__name__ + '.tweets_scrapper.logger')
    def testActuallySavesData(self, mock_logger):
        mock_logger.login = Mock(return_value = self.mock_API)
        chunkSaver = tweets_scrapper.ChunkSaver()
        chunkSaver.save(['id0','id1'])
        self.assertTrue(models.Tweet.objects.filter(tweet_id = 'id0', retweets = 0, likes = 1).exists())
        self.assertTrue(models.Tweet.objects.filter(tweet_id = 'id1', retweets = 2, likes = 3).exists())        
        
        
        
        
