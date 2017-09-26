from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Tweet(models.Model):
	tweet_id = models.CharField(max_length = 255, unique =  True)
	in_reply_to_status_id = models.CharField(max_length = 255)
	in_reply_to_user_id = models.CharField(max_length = 255)
	timestamp = models.DateTimeField()
	source = models.CharField(max_length = 255)
	text = models.CharField(max_length = 255)
	expanded_urls = models.CharField(max_length = 255)
	likes = models.IntegerField(null=True)
	retweets = models.IntegerField(null=True) 
	responses = models.IntegerField(null=True)
	exists_in_twitter = models.BooleanField(default=True)

	def url(self):
		return '<a target="_blank" href="https://twitter.com/statuses/%s">link to tweet</a>' % (self.tweet_id)

	url.short_description = 'Url'
	url.allow_tags = True

	def is_response(self):
		return not in_reply_to_status_id == "";
