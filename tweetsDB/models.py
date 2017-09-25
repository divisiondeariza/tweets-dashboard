from __future__ import unicode_literals

from django.db import models

# Create your models here.

class tweet(models.Model):
	tweet_id = models.CharField(max_length = 255)
	in_reply_to_status_id = models.CharField(max_length = 255)
	in_reply_to_user_id = models.CharField(max_length = 255)
	timestamp = models.DateTimeField()
	source = models.CharField(max_length = 255)
	text = models.CharField(max_length = 255)
	expanded_urls = models.CharField(max_length = 255)
	likes = models.IntegerField()
	retweets = models.IntegerField() 
	responses = models.IntegerField()
