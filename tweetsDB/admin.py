from django.contrib import admin
from tweetsDB import models
from libs.twitter_utils import tweets_destroyer
from rangefilter.filter import DateRangeFilter
from advanced_filters.admin import AdminAdvancedFiltersMixin
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _


class IsResponseFilter(admin.SimpleListFilter):
	title = _('Is Response')

	parameter_name = 'in_reply_to_user_id'

	def lookups(self, request, model_admin):
		return (
			('true', _('Yes')),
			('false', _('No')),
		)

	def queryset(self, request, queryset):

		if self.value() == 'true':
			return queryset.filter(~Q(in_reply_to_user_id = "") | ~Q(in_reply_to_status_id = "") )
		if self.value() == 'false':
			return queryset.filter(Q(in_reply_to_user_id = "") & Q(in_reply_to_status_id = ""))
	

class inlineRatingAdmin(admin.TabularInline):
	model = models.RatingScore
	extra = 0


@admin.register(models.Tweet)
class TweetAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
	inlines = [inlineRatingAdmin]
	list_display  = ('text', 'likes_count', 'retweets_count', 'timestamp', 'url', 'exists_in_twitter',
					 'in_reply_to_user_id', 'mean_rating')
	readonly_fields = ('text', 'likes_count', 'retweets_count', 'timestamp', 'url', 'exists_in_twitter', 
					   'in_reply_to_user_id', 'tweet_id', 'in_reply_to_status_id',
 					   'retweeted_status_id', 'retweeted_status_user_id', 'retweeted_status_timestamp',
 					   'source', 'expanded_urls', 'responses', 'mean_rating')
	list_filter = (('timestamp', DateRangeFilter), 'exists_in_twitter', IsResponseFilter, 'tags')
	advanced_filter_fields = ('timestamp', 'exists_in_twitter', 'likes', 'retweets', 'is_response', 'mean_rating')
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