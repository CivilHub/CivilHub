# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Category, Invitation, Organization


class InvitationAdmin(admin.ModelAdmin):
    readonly_fields = ('key', 'is_accepted', 'date_accepted', )


class OrganizationAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', )


admin.site.register(Category)
admin.site.register(Invitation, InvitationAdmin)
admin.site.register(Organization, OrganizationAdmin)
