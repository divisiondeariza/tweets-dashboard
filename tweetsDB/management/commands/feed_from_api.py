from django.core.management.base import BaseCommand
from libs.twitter_utils.tweets_scrapper import TweetsScrapper

class Command(BaseCommand):
	help = 'populates tweets in database with api tweets'

	def add_arguments(self, parser):
		parser.add_argument('--update-all', action='store_true')
		
	def handle(self, *args, **options):
		scrapper = TweetsScrapper()
		scrapper.populate_db(only_not_scrapped = not options['update_all'])
