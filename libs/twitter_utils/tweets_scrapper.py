import logger
from tweetsDB import models

class ChunkSaver(object):
    def save(self, ids):
        API = logger.login()
        retrieved_statuses = API.statuses_lookup(ids)
        for status in retrieved_statuses:
            tweet = models.Tweet.objects.get(tweet_id = status.id)
            tweet.retweets = status.retweet_count
            tweet.likes =  status.favorite_count
            tweet.save()
