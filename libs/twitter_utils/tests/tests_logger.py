'''
Created on 1/10/2017

@author: emmanuel
'''
import unittest
from .. import logger, secrets 
import tweepy
from mock.mock import patch, Mock

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass

    @patch(__name__ + '.logger.tweepy')
    def testLoginUsesKeysCorrectly(self, mock_tweepy):
        mock_auth = Mock()
        mock_tweepy.OAuthHandler = Mock(return_value = mock_auth)
        logger.login()
        mock_tweepy.OAuthHandler.assert_called_once_with(secrets.consumer_key, secrets.consumer_secret)
        mock_auth.set_access_token.assert_called_once_with(secrets.access_token, secrets.access_token_secret)
    
    @patch(__name__ + '.logger.tweepy')    
    def testLoginCreatesTweepyApi(self, mock_tweepy):
        mock_auth = Mock()
        mock_tweepy.OAuthHandler = Mock(return_value = mock_auth)
        logger.login()
        mock_tweepy.API.assert_called_once_with(mock_auth)
        

    @patch(__name__ + '.logger.tweepy')   
    def testLoginReturnsApi(self, mock_tweepy):
        mock_api = Mock()
        mock_tweepy.API = Mock(return_value = mock_api)      
        self.assertEqual(mock_api, logger.login())    
        