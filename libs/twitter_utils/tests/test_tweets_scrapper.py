'''
Created on 1/10/2017

@author: emmanuel
'''
import unittest
from tweetsDB import models
from .. import tweets_scrapper 
from unittest.case import skip
from mock.mock import patch, Mock, call
from django.test.testcases import TestCase

class Status_mock():
    def __init__(self, id, retweets, likes):
        self.id = id
        self.text = "some text from {0}".format(id)
        self.retweet_count = retweets
        self.favorite_count = likes 

class TestTweetsScrapper(unittest.TestCase):


    def setUp(self):
        pass
        for i in range(200):
            tweet, tweetWasCreated = models.Tweet.objects.get_or_create(tweet_id = "dummyid{0}".format(i),
                                                                        created_at = "2017-09-25 13:41:10+0000")


    def tearDown(self):
        pass

    @patch(__name__ + '.tweets_scrapper.ChunkSaver')
    def testCallsChunkSaverCorrectly(self, mock_chunk_saver):
        scrapper = tweets_scrapper.TweetsScrapper()
        scrapper.populate_db()
        expected_calls = [call(["dummyid{0}".format(i) for i in range(100) ]), 
                          call(["dummyid{0}".format(i + 100) for i in range(100) ])]
        mock_chunk_saver().save.assert_has_calls(expected_calls)
 
    
    @patch(__name__ + '.tweets_scrapper.ChunkSaver')
    def testChunkSaverIsCreatedOnce(self, mock_chunk_saver):
        scrapper = tweets_scrapper.TweetsScrapper()
        scrapper.populate_db()
        scrapper.populate_db()
        mock_chunk_saver.assert_called_once()

    @patch(__name__ + '.tweets_scrapper.logger')        
    def testScrapsOnlyNotScrappedWhenOnlyNotScrappedOptionIsGiven(self, mock_logger):
        mock_API = Mock()
        mock_API.statuses_lookup = Mock(return_value = [Status_mock('dummyid0', 0, 1),
                                                        Status_mock('dummyid1', 2, 3)])
        mock_logger.login = Mock(return_value = mock_API)
        scrapper = tweets_scrapper.TweetsScrapper()
        scrapper.populate_db()
        for i in range(100):
            tweet, tweetWasCreated = models.Tweet.objects.get_or_create(tweet_id = "dummyid{0}".format(i+200),
                                                                        created_at = "2017-09-25 13:41:10+0000")
        mock_API.statuses_lookup.reset_mock() 
        scrapper.populate_db(only_not_scrapped = True)
        mock_API.statuses_lookup.assert_called_once_with([u"dummyid{0}".format(i + 200) for i in range(100) ])
    
class TestChunkSaver(TestCase):


    def setUp(self):
        for i in range(4):
            tweet = models.Tweet.objects.create(tweet_id = "id{0}".format(i),
                                                created_at = "2017-09-25 13:41:10+0000")
            
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
        self.assertTrue(models.Tweet.objects.filter(tweet_id = 'id0', retweets_count = 0, likes_count = 1).exists())
        self.assertTrue(models.Tweet.objects.filter(tweet_id = 'id1', retweets_count = 2, likes_count = 3).exists())        
        
    @patch(__name__ + '.tweets_scrapper.logger')
    def testCreatesOnlyOneAprPerInstance(self, mock_logger):
        mock_logger.login = Mock(return_value = self.mock_API)
        chunkSaver = tweets_scrapper.ChunkSaver()
        chunkSaver.save(['id0','id1'])
        chunkSaver.save(['id1','id2'])
        mock_logger.login.assert_called_once()

    @patch(__name__ + '.tweets_scrapper.logger')
    def testMarkTweetsNotInRetrievedArrayAsNonExistent(self, mock_logger):
        mock_logger.login = Mock(return_value = self.mock_API)
        chunkSaver = tweets_scrapper.ChunkSaver()
        chunkSaver.save(['id0','id1','id2'])
        self.assertTrue(models.Tweet.objects.get(tweet_id = 'id1').exists_in_twitter)
        self.assertFalse(models.Tweet.objects.get(tweet_id = 'id2').exists_in_twitter)
        

        
        
        
        
        
        
        
        
