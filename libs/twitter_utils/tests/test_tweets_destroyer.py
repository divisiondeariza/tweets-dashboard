'''
Created on 2/10/2017

@author: emmanuel
'''
import unittest
from .. import tweets_destroyer
from mock.mock import Mock, patch, call
from unittest.case import skip
from django.test.testcases import TestCase
from tweetsDB import models
from tweepy.error import TweepError


class Test(TestCase):


    def setUp(self):
        self.mock_API = Mock()
        for i in range(5):
            models.Tweet.objects.create(tweet_id = "id{0}".format(i),
                                        timestamp = "2017-09-25 13:41:10+0000")


    def tearDown(self):
        pass

    @patch(__name__ + '.tweets_destroyer.logger')
    def testDeletesTweetsInIdsList(self, mock_logger):
        mock_logger.login = Mock(return_value = self.mock_API)
        destroyer = tweets_destroyer.Destroyer()
        query = models.Tweet.objects.all()[0:3]
        destroyer.destroy(query)
        expected_calls = [call(u'id0'), call(u'id1'), call(u'id2')] 
        self.mock_API.destroy_status.assert_has_calls(expected_calls, any_order=False)

    @patch(__name__ + '.tweets_destroyer.logger')
    def testCreatesOnlyOneAprPerInstance(self, mock_logger):
        mock_logger.login = Mock(return_value = self.mock_API)
        destroyer = tweets_destroyer.Destroyer()
        all_tweets = models.Tweet.objects.all()[0:3]
        destroyer.destroy(all_tweets[0:3])
        destroyer.destroy(all_tweets[3:])
        mock_logger.login.assert_called_once()
      
    @patch(__name__ + '.tweets_destroyer.logger')
    def testSetsExistsInTwitterFalse(self, mock_logger):
        mock_logger.login = Mock(return_value = self.mock_API)
        destroyer = tweets_destroyer.Destroyer()
        query = models.Tweet.objects.filter(tweet_id = "id1")
        destroyer.destroy(query)
        self.assertFalse(models.Tweet.objects.get(tweet_id = "id1").exists_in_twitter)

    @patch(__name__ + '.tweets_destroyer.logger')
    def testSetsExistsInTwitterFalseEvenIfTweetsDoesNotExists(self, mock_logger):
        mock_logger.login = Mock(return_value = self.mock_API)
        self.mock_API.destroy_status.side_effect = TweepError("status does not exists")
        destroyer = tweets_destroyer.Destroyer()
        query = models.Tweet.objects.filter(tweet_id = "id1")
        destroyer.destroy(query)
        self.assertFalse(models.Tweet.objects.get(tweet_id = "id1").exists_in_twitter)
