from django.contrib import admin
from tweetsDB import models
from read_only_admin.admin import ReadonlyAdmin


class ReadOnlyAdminBase(ReadonlyAdmin):

    def get_readonly_fields(self, request, obj=None):
        print [f.name for f in self.model._meta.fields if f.name not in ["id"]]
        return self.fields or [f.name for f in self.model._meta.fields if f.name not in ["id"]]
    
    def has_add_permission(self, request):
        return False
         
    def has_delete_permission(self, request, obj=None):
        return False       



@admin.register(models.Tweet)
class TweetAdmin(ReadOnlyAdminBase):
	list_display  = ('text', 'likes', 'retweets', 'responses', 'timestamp', 'url')
	list_filter = ('likes', 'retweets', 'responses')

	def get_readonly_fields(self, request, obj=None):
		read_only = ReadOnlyAdminBase.get_readonly_fields(self, request, obj=obj) + ['url']
		read_only.remove('source') 
		return read_only

