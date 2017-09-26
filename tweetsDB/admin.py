from django.contrib import admin
from tweetsDB import models, logger
from read_only_admin.admin import ReadonlyAdmin
from rangefilter.filter import DateRangeFilter
from advanced_filters.admin import AdminAdvancedFiltersMixin
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

def destroy_tweets(modeladmin, request, queryset):
	pass
	
class IsResponseFilter(admin.SimpleListFilter):
	title = _('Is Response')

	parameter_name = 'in_reply_to_status_id'

	def lookups(self, request, model_admin):
		return (
			('true', _('Yes')),
			('false', _('No')),
		)

	def queryset(self, request, queryset):

		if self.value() == 'true':
			return queryset.filter(~Q(in_reply_to_status_id = ""))
		if self.value() == 'false':
			return queryset.filter(Q(in_reply_to_status_id = ""))
	
	

@admin.register(models.Tweet)
class TweetAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
	list_display  = ('text', 'likes', 'retweets', 'responses', 'timestamp', 'url')
	list_filter = (('timestamp', DateRangeFilter), 'exists_in_twitter', IsResponseFilter)
	advanced_filter_fields = ('timestamp', 'exists_in_twitter', 'likes', 'retweets', 'is_response')
	actions = ['destroy_tweets']
	list_per_page = 500

	def has_add_permission(self, request):
		return False
		 
	def has_delete_permission(self, request, obj=None):
		return False       

