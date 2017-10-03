from django.core.management.base import BaseCommand
from django.db import transaction
from libs.twitter_utils import csv_loader

class Command(BaseCommand):
    help = 'populates db from tweets.csv'
    
    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)
    
    @transaction.atomic
    def handle(self, *args, **options):
        loader = csv_loader.Loader()
        loader.load(options['filename'])

