from django.contrib import admin
from tweetsDB import models

# Register your models here.
@admin.register(models.Tweet)
class TweetAdmin(admin.ModelAdmin):
	list_display  = ('text', 'likes', 'retweets', 'responses', 'timestamp', 'url')
	list_filter = ('likes', 'retweets', 'responses')

	

