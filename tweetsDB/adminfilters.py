'''
Created on 7/10/2017

@author: emmanuel
'''
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.db.models.query_utils import Q


class IsResponseFilter(admin.SimpleListFilter):
    title = _('Is Response')
    parameter_name = 'is_response'
    
    def lookups(self, request, model_admin):
        return (
            ('yes', _('Yes')),
            ('no', _('No')),
        )
        
    def queryset(self, request, queryset):

        if self.value() == 'yes':
            return queryset.filter((~Q(in_reply_to_user_id = "") & ~Q(in_reply_to_user_id = None))| 
                                   (~Q(in_reply_to_status_id = "") & ~Q(in_reply_to_status_id = None)))
            
        if self.value() == 'no':
            return queryset.filter((Q(in_reply_to_user_id = "") | Q(in_reply_to_user_id = None)) & 
                                   (Q(in_reply_to_status_id = "") | Q(in_reply_to_status_id = None)))
        elif self.value():
            return queryset.none() 
        


class IsRetweetFilter(admin.SimpleListFilter):
    title = _('Is Retweet')
    parameter_name = 'is_retweet'
    
    def lookups(self, request, model_admin):
        return (
            ('yes', _('Yes')),
            ('no', _('No')),
        )    

    def queryset(self, request, queryset):

        if self.value() == 'yes':
            return queryset.filter((~Q(retweeted_status_id = "") & ~Q(retweeted_status_id = None)))

        if self.value() == 'no':
            return queryset.filter(Q(retweeted_status_id = "") | Q(retweeted_status_id = None))
        
        elif self.value():
            return queryset.none() 

