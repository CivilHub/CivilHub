from django.contrib import admin
from .models import LoginData, RegisterDemand, UserProfile, Badge

admin.site.register(LoginData)
admin.site.register(RegisterDemand)
admin.site.register(UserProfile)
admin.site.register(Badge)
