from django.core.management.base import BaseCommand, CommandError
from tweetsDB import models
from libs.twitter_utils import logger
from django.db import transaction


class Command(BaseCommand):
	help = 'populates tweets in database with api tweets'
    
	def handle(self, *args, **options):
		tweets = models.Tweet.objects.filter(	likes__isnull = True,
												retweets__isnull = True,
												#responses__isnull = True,
												)
		tweets_ids = [tweet.tweet_id for tweet in tweets]
		print "there are {0} tweets without likes and retweets data".format(len(tweets_ids))
		twapi =  logger.login()
		for ids_chunk in self.chunks(tweets_ids, 100):
			self.save_chunk(ids_chunk, twapi)


	
	def chunks(self, array, length):
		"""Yield successive n-sized chunks from l."""
		for i in range(0, len(array), length):
			yield array[i:i + length]
	
	@transaction.atomic
	def save_chunk(self, ids_chunk, twapi):
		api_tweets = twapi.statuses_lookup(ids_chunk)

		for api_tweet in api_tweets:
			print "saving data for tweet: " + api_tweet.text
			print "retweets: {0}, likes: {0}".format(api_tweet.retweet_count, api_tweet.favorite_count)
			print api_tweet.id
			tweet = models.Tweet.objects.get(tweet_id = api_tweet.id)
			tweet.retweets = api_tweet.retweet_count
			tweet.likes = api_tweet.favorite_count
			tweet.save()
