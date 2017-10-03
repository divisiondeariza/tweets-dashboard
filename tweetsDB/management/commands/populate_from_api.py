from django.core.management.base import BaseCommand
from libs.twitter_utils import tweets_scrapper


class Command(BaseCommand):
	help = 'populates tweets in database with api tweets'
	
	def handle(self, *args, **options):
		scrapper = tweets_scrapper.TweetsScrapper()
		scrapper.populate_db()
