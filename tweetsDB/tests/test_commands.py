'''
Created on 5/10/2017

@author: emmanuel
'''
from django.core.management import call_command
from django.test.testcases import TestCase
from mock.mock import patch
from tweetsDB.management.commands import populate, feed_from_api


class TestPopulateCommand(TestCase):
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch(__name__ + '.populate.TimelineSaver')
    @patch(__name__ + '.populate.Loader')
    def testPopulatesFromApiByDefault(self, mock_loader, mock_timeline_saver):
        call_command('populate')
        mock_timeline_saver().save.assert_called_once()
        mock_loader().load.assert_not_called()
    
    @patch(__name__ + '.populate.TimelineSaver')    
    @patch(__name__ + '.populate.Loader')
    def testPopulatesFromFileWhenFromFileOptionSet(self, mock_loader, mock_timeline_saver):
        call_command('populate', '--from-file', 'filename.csv')
        mock_loader().load.assert_called_once_with('filename.csv')
        mock_timeline_saver().save.assert_not_called()


class TestFeedFromApiCommand(TestCase):
    
    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    @patch(__name__ + '.feed_from_api.TweetsScrapper')
    def testCallsTweetsScrapperCorrectlyByDefault(self, mock_tweets_scrapper):
        call_command('feed_from_api')
        mock_tweets_scrapper().populate_db.assert_called_once_with(only_not_scrapped = True)

    @patch(__name__ + '.feed_from_api.TweetsScrapper')
    def testCallsTweetsScrapperCorrectlyWhenUpdateAllRequired(self, mock_tweets_scrapper):
        call_command('feed_from_api', '--update-all')
        mock_tweets_scrapper().populate_db.assert_called_once_with(only_not_scrapped = False)        
    
    
    