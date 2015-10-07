# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Voting, Marker, Vote


class VotingAdmin(admin.ModelAdmin):
    list_display = ('label', 'author', 'is_public', 'is_limited',)
    list_filter = ('created_at',)
    search_fields = ('label', 'description',)

admin.site.register(Voting, VotingAdmin)


class MarkerAdmin(admin.ModelAdmin):
    list_filter = ('voting',)

admin.site.register(Marker, MarkerAdmin)


class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'marker', 'date',)
    list_filter = ('marker__voting',)
    search_fields = ('user__first_name', 'user__last_name', 'user__email',)

admin.site.register(Vote, VoteAdmin)

