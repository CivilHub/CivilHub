# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext as _

from models import Idea, Category, Vote


admin.site.register(Category)

class VoteAdmin(admin.ModelAdmin):
    list_display = ('idea', 'user', 'get_username', 'status', 'date_voted', )
    search_fields = ('idea__name', )

    def get_username(self, obj):
        return obj.user.get_full_name()
    get_username.short_description = _(u"user full name")

admin.site.register(Vote, VoteAdmin)


class IdeaAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_filter = ('date_created', )
    list_display = ('__unicode__', 'get_username', 'location', 'date_created', )
    raw_id_fields = ('location', )

    def get_username(self, obj):
        return obj.creator.get_full_name()
    get_username.short_description = _(u"user")

admin.site.register(Idea, IdeaAdmin)
