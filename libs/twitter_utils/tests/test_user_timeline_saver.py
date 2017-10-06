'''
Created on 4/10/2017

@author: emmanuel
'''
import unittest
from .. import user_timeline_saver
from mock.mock import patch, Mock
import datetime
from tweetsDB import models
from django.test.testcases import TestCase

class MockAuthor():
    def __init__(self):
        self.id = "someauthorid"

class MockStatus():
    
    def __init__(self, tweet_id, is_retweet = False):
        self.id = str(tweet_id)
        self.in_reply_to_status_id = "someid"
        self.in_reply_to_user_id = "someuserid"
        self.created_at = datetime.datetime(2017, 10, 5, 3, 49, 43)
        self.source =  'Twitter Web Client'
        self.text = "text of tweet {0}".format(tweet_id)
        self.retweet_count = 5
        self.favorite_count = 10
        self.retweeted = is_retweet
        self.author = MockAuthor()
        if is_retweet:
            self.retweeted_status = MockStatus(self.id + "R")
    
        

class Test(TestCase):


    def setUp(self):
        self.mock_API = Mock()
        #self.mock_API.user_timeline.side_effect = [response1,response2,[]]
        self.response1 = MockStatus('id1')
        self.response2 = MockStatus('id2', True)



    def tearDown(self):
        pass

    @patch(__name__ + '.user_timeline_saver.tweepy')   
    @patch(__name__ + '.user_timeline_saver.logger')
    def testCreatesOnlyOneApiPerInstance(self, mock_logger, mock_tweepy):
        mock_logger.login = Mock(return_value = self.mock_API)
        saver = user_timeline_saver.TimelineSaver()
        saver.save()
        saver.save()
        mock_logger.login.assert_called_once()
    
    @patch(__name__ + '.user_timeline_saver.tweepy')    
    @patch(__name__ + '.user_timeline_saver.logger')
    def testSaveTweetsRetrieved(self, mock_logger, mock_tweepy):
        mock_logger.login = Mock(return_value = self.mock_API)
        mock_tweepy.Cursor().items.return_value = [self.response1,self.response2]
        saver = user_timeline_saver.TimelineSaver()
        saver.save()
        self.assertTrue(models.Tweet.objects.filter(tweet_id = 'id1',
                                                    in_reply_to_status_id = 'someid',
                                                    in_reply_to_user_id = 'someuserid',
                                                    created_at = '2017-10-05 03:49:43+0000',
                                                    source =  'Twitter Web Client',
                                                    text = "text of tweet id1",
                                                    retweets_count = 5,
                                                    likes_count = 10,
                                                    retweeted_status_id = "",
                                                    retweeted_status_user_id = "",
                                                    retweeted_status_created_at = None).exists())
        
        self.assertTrue(models.Tweet.objects.filter(tweet_id = 'id2',
                                                    in_reply_to_status_id = 'someid',
                                                    in_reply_to_user_id = 'someuserid',
                                                    created_at = '2017-10-05 03:49:43+0000',
                                                    source =  'Twitter Web Client',
                                                    text = "text of tweet id2",
                                                    retweets_count = 5,
                                                    likes_count = 10,
                                                    retweeted_status_id = "id2R",
                                                    retweeted_status_user_id = "someauthorid",
                                                    retweeted_status_created_at = '2017-10-05 03:49:43+0000',
                                                    ).exists())    
    @patch(__name__ + '.user_timeline_saver.tweepy')    
    @patch(__name__ + '.user_timeline_saver.logger')    
    def testUpdatesAlreadySavedStatus(self, mock_logger, mock_tweepy):
        mock_logger.login = Mock(return_value = self.mock_API)
        mock_tweepy.Cursor().items.return_value = [self.response1,self.response2]
        saver = user_timeline_saver.TimelineSaver()
        saver.save()
        self.response1.retweet_count = 10
        saver.save()
        self.assertEqual(models.Tweet.objects.get(tweet_id = "id1").retweets_count, 10)
        


