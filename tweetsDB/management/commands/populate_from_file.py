from django.core.management.base import BaseCommand, CommandError
from tweetsDB import models
import csv
from django.db import transaction

class Command(BaseCommand):
    help = 'populates db from tweets.csv'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)

    @transaction.atomic
    def handle(self, *args, **options):
        with open(options['filename'], 'rb') as csvfile:
				reader = csv.DictReader(csvfile)
				for row in reader:
					if not row['retweeted_status_id']:
						tweet, tweetWasCreated = models.Tweet.objects.get_or_create(tweet_id = row['tweet_id'])
						tweet.in_reply_to_status_id =  row['in_reply_to_status_id']
						tweet.in_reply_to_user_id = row['in_reply_to_user_id']
						tweet.timestamp = row['timestamp'].split(" +")[0]
						tweet.source = row['source']
						tweet.text = row['text']
						tweet.expanded_urls = row['expanded_urls']
						tweet.save()
					
