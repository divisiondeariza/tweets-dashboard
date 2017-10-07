from __future__ import unicode_literals

from django.db import models
from taggit.managers import TaggableManager
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Rating(models.Model):
	weight = models.FloatField(default = 1,
								validators=[MaxValueValidator(1), MinValueValidator(0)])
	name = models.CharField(max_length = 255)
	
	def __unicode__(self):
		return "{0} ({1})".format(self.name, self.weight)



class RatingScore(models.Model):
	tweet = models.ForeignKey('Tweet', on_delete=models.CASCADE, related_name="rating_score")
	group = models.ForeignKey('Rating', on_delete=models.CASCADE, related_name="rating_score")
	score = models.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(0)])


class Tweet(models.Model):
	tweet_id = models.TextField(max_length = 255, unique =  True)
	in_reply_to_status_id = models.CharField(max_length = 255, null=True, default ="")
	in_reply_to_user_id = models.CharField(max_length = 255, null=True, default ="")
	created_at = models.DateTimeField(null=True)
	source = models.CharField(max_length = 255, null=True, default ="")
	text = models.CharField(max_length = 255, null=True, default ="")
	retweeted_status_id = models.CharField(max_length = 255, null=True, default ="")	
	retweeted_status_user_id = models.CharField(max_length = 255, null=True, default ="")
	retweeted_status_created_at = models.DateTimeField(null=True)
	expanded_urls = models.CharField(max_length = 255, null=True, default ="")
	
	likes_count = models.IntegerField(null=True)
	retweets_count = models.IntegerField(null=True) 
	responses = models.IntegerField(null=True)
	exists_in_twitter = models.BooleanField(default=True)
	tags = TaggableManager(blank=True)
	ratings = models.ManyToManyField(Rating, through='RatingScore')

	def url(self):
		return '<a target="_blank" href="https://twitter.com/statuses/%s">link to tweet</a>' % (self.tweet_id)

	url.short_description = 'Url tag'
	url.allow_tags = True

	def is_response(self):
		return not self.in_reply_to_status_id == "";
	
	def mean_rating(self):
		sum_of_weights = 0
		weighted_sum = 0
		for rating in self.ratings.all():
			sum_of_weights += rating.weight
			weighted_sum += rating.weight*rating.rating_score.get(tweet = self).score
		if sum_of_weights == 0:
			return 0
		return weighted_sum/sum_of_weights
		
			

	

	



	