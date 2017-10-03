'''
Created on 2/10/2017

@author: emmanuel
'''
import unittest
from mock.mock import patch, mock_open
from mock import mock
from .. import csv_loader
from unittest.case import skip
from tweetsDB import models


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass

    @patch(__name__ + '.csv_loader.open', create=True)
    def testOpensCorrectFile(self, m_open):
        loader = csv_loader.Loader()
        loader.load('filename')
        m_open.assert_called_once_with('filename','rb')
  
    @patch(__name__ + '.csv_loader.open', create=True)
    def testOpensCorrectFilee(self, m_open):
        loader = csv_loader.Loader()
        loader.load('filename')
        m_open.assert_called_once_with('filename','rb')
        

    def testLoadsData(self):
        file_content = 'tweet_id,in_reply_to_status_id,in_reply_to_user_id,timestamp,source,text,retweeted_status_id,retweeted_status_user_id,retweeted_status_timestamp,expanded_urls\nid100,xx,xx,2017-09-25 13:41:10 +0000,"<a href=""http://twitter.com"" rel=""nofollow"">Twitter Web Client</a>",this is a tweet,xx,xx,2017-09-25 13:33:07 +0000,\nid1,xx,xx,2017-09-25 13:25:11 +0000,"<a href=""http://twitter.com"" rel=""nofollow"">Twitter Web Client</a>",this is another tweet,,,,https://twitter.com/DivisionDeAriza/status/912306991871250440/photo/1'
       
        with patch(__name__ + '.csv_loader.open', mock_open(read_data=file_content)) as m_open:
            m_open.return_value.__iter__ = lambda self: iter(self.readline, '')
            m_open.return_value.__next__ = lambda self: next(iter(self.readline, ''))       
            loader = csv_loader.Loader()
            loader.load('filename')
        self.assertTrue(models.Tweet.objects.filter(tweet_id = 'id100', 
                                                    in_reply_to_status_id = 'xx',
                                                    in_reply_to_user_id =  'xx',
                                                    timestamp = "2017-09-25 13:41:10+0000",
                                                    source = '<a href="http://twitter.com" rel="nofollow">Twitter Web Client</a>',
                                                    text = 'this is a tweet',
                                                    retweeted_status_id = 'xx',
                                                    retweeted_status_user_id = 'xx',    
                                                    retweeted_status_timestamp = '2017-09-25 13:33:07+0000',
                                                    expanded_urls = '').exists())

        self.assertTrue(models.Tweet.objects.filter(tweet_id = 'id1', 
                                                    in_reply_to_status_id = 'xx',
                                                    in_reply_to_user_id =  'xx',
                                                    timestamp = "2017-09-25 13:25:11+0000",
                                                    source = '<a href="http://twitter.com" rel="nofollow">Twitter Web Client</a>',
                                                    text = 'this is another tweet',
                                                    retweeted_status_id = '',
                                                    retweeted_status_user_id = '',    
                                                    retweeted_status_timestamp = None,
                                                    expanded_urls = 'https://twitter.com/DivisionDeAriza/status/912306991871250440/photo/1'
                                                    ).exists())        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()