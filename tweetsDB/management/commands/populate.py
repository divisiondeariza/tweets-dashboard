from django.core.management.base import BaseCommand
from libs.twitter_utils.user_timeline_saver import TimelineSaver
from libs.twitter_utils.csv_loader import Loader

class Command(BaseCommand):
    help = 'populates db from tweets.csv'
    
    def add_arguments(self, parser):
        parser.add_argument('--from-api', action='store_true')    
        parser.add_argument('--from-file', type=str, required=False)

    def handle(self, *args, **options):
        if options['from_file']:
            loader = Loader()
            loader.load(options['from_file'])
        else:
            timeline_saver = TimelineSaver()
            timeline_saver.save()
        
