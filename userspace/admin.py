# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import LoginData, RegisterDemand, UserProfile, Badge


class UserProfileAdmin(admin.ModelAdmin):
	model = UserProfile
	list_display = ('full_name', 'email', 'date_joined',)
	list_filter = ('user__date_joined',)
	search_fields = ('user__username', 'user__first_name',
					 'user__last_name', 'user__email')

	def email(self, obj):
		return obj.user.email

	def full_name(self, obj):
		return obj.user.get_full_name()

	def date_joined(self, obj):
		return obj.user.date_joined


admin.site.register(LoginData)
admin.site.register(RegisterDemand)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Badge)
