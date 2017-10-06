import logger
from tweetsDB import models
from django.db import transaction


class TweetsScrapper(object):
    
    def __init__(self):
        self.chunk_saver = ChunkSaver()

    def populate_db(self, only_not_scrapped = False):
        query = self._get_query(only_not_scrapped)
        tweets_ids = self._get_tweets_ids(query)
        for i in range(0, len(tweets_ids), 100):
            self.chunk_saver.save(tweets_ids[i:i + 100]) 


    def _get_query(self, only_not_scrapped):
        if only_not_scrapped:
            query = models.Tweet.objects.filter(exists_in_twitter=True, likes=None)
        else:
            query = models.Tweet.objects.all()
        return query
    
    def _get_tweets_ids(self, query):
        tweets_ids = [tweet.tweet_id for tweet in query]
        return tweets_ids
    
    
@transaction.atomic 
class ChunkSaver(object):
    
    def __init__(self):
        self.API = logger.login()

    def save(self, ids):
        retrieved_statuses = self.API.statuses_lookup(ids)
        for status in retrieved_statuses:
            self._save_single_tweet(status)
        self._mark_not_found_tweets_as_non_existent(ids, retrieved_statuses)

    def _mark_not_found_tweets_as_non_existent(self, ids, retrieved_statuses):
        retrieved_ids = [status.id for status in retrieved_statuses]
        not_found_ids = [tweet_id for tweet_id in ids if not tweet_id in retrieved_ids]
        for tweet_id in not_found_ids:
            self._mark_id_as_non_existent(tweet_id)    

    def _save_single_tweet(self, status):
        tweet = models.Tweet.objects.get(tweet_id=status.id)
        tweet.retweets = status.retweet_count
        tweet.likes_count = status.favorite_count
        tweet.save()

    def _mark_id_as_non_existent(self, tweet_id):
        tweet = models.Tweet.objects.get(tweet_id=tweet_id)
        tweet.exists_in_twitter = False
        tweet.save()





