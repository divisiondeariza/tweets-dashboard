from django.contrib import admin
from tweetsDB import models
from libs.twitter_utils import tweets_destroyer
from rangefilter.filter import DateRangeFilter
from advanced_filters.admin import AdminAdvancedFiltersMixin
from tweetsDB.adminfilters import IsResponseFilter, IsRetweetFilter

class inlineRatingAdmin(admin.TabularInline):
	model = models.RatingScore
	extra = 0


@admin.register(models.Tweet)
class TweetAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
	inlines = [inlineRatingAdmin]
	list_display  = ('text', 'likes_count', 'retweets_count', 'created_at', 'url', 'exists_in_twitter',
					 'in_reply_to_user_id', 'mean_rating')
	readonly_fields = ('text', 'likes_count', 'retweets_count', 'created_at', 'url', 'exists_in_twitter', 
					   'in_reply_to_user_id', 'tweet_id', 'in_reply_to_status_id',
 					   'retweeted_status_id', 'retweeted_status_user_id', 'retweeted_status_created_at',
 					   'source', 'expanded_urls', 'responses', 'mean_rating')
	list_filter = (('created_at', DateRangeFilter), 'exists_in_twitter', IsResponseFilter, IsRetweetFilter, 'tags')
	advanced_filter_fields = ('created_at', 'exists_in_twitter', 'likes_count', 'retweets_count', 'is_response', 'mean_rating')
	actions = ['destroy_tweets']
	search_fields = ['text']
	list_per_page = 990
	
	destroyer = tweets_destroyer.Destroyer()
	
	def destroy_tweets(self, request, queryset):
		self.destroyer.destroy(queryset)
			

	def has_add_permission(self, request):
		return False

	def has_delete_permission(self, request, obj=None):
		return False       

	def get_actions(self, request):
		actions = super(TweetAdmin, self).get_actions(request)
		if 'delete_selected' in actions:
			del actions['delete_selected']
		return actions


admin.site.register(models.Rating)