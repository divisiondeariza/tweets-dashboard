import logger
from tweetsDB import models


class TweetsScrapper(object):
    
    def __init__(self):
        self.chunk_saver = ChunkSaver()


    def populate_db(self):
        tweets_ids = self._get_tweets_ids()
        for i in range(0, len(tweets_ids), 100):
            self.chunk_saver.save(tweets_ids[i:i + 100]) 

    def _get_tweets_ids(self):
        tweets = models.Tweet.objects.all()
        tweets_ids = [tweet.tweet_id for tweet in tweets]
        return tweets_ids

class ChunkSaver(object):
    
    def __init__(self):
        self.API = logger.login()

    def save(self, ids):
        retrieved_statuses = self.API.statuses_lookup(ids)
        for status in retrieved_statuses:
            self._save_single_tweet(status)

    def _save_single_tweet(self, status):
        tweet = models.Tweet.objects.get(tweet_id=status.id)
        tweet.retweets = status.retweet_count
        tweet.likes = status.favorite_count
        tweet.save()
        



