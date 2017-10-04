from __future__ import unicode_literals

from django.db import models
from taggit.managers import TaggableManager
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Rating(models.Model):
	weight = models.FloatField(default = 1,
								validators=[MaxValueValidator(1), MinValueValidator(0)])
	name = models.CharField(max_length = 255)


class RatingScore(models.Model):
	tweet = models.ForeignKey('Tweet', on_delete=models.CASCADE, related_name="ratingScore")
	group = models.ForeignKey('Rating', on_delete=models.CASCADE)
	score = models.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(0)])


class Tweet(models.Model):
	tweet_id = models.CharField(max_length = 255, unique =  True)
	in_reply_to_status_id = models.CharField(max_length = 255)
	in_reply_to_user_id = models.CharField(max_length = 255)
	timestamp = models.DateTimeField(null=True)
	source = models.CharField(max_length = 255)
	text = models.CharField(max_length = 255)
	retweeted_status_id = models.CharField(max_length = 255)	
	retweeted_status_user_id = models.CharField(max_length = 255)
	retweeted_status_timestamp = models.DateTimeField(null=True)
	expanded_urls = models.CharField(max_length = 255)
	
	likes = models.IntegerField(null=True)
	retweets = models.IntegerField(null=True) 
	responses = models.IntegerField(null=True)
	exists_in_twitter = models.BooleanField(default=True)
	tags = TaggableManager()
	ratings = models.ManyToManyField(Rating, through='RatingScore')

	def url(self):
		return '<a target="_blank" href="https://twitter.com/statuses/%s">link to tweet</a>' % (self.tweet_id)

	url.short_description = 'Url tag'
	url.allow_tags = True

	def is_response(self):
		return not self.in_reply_to_status_id == "";

	

	



	