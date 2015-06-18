from django.contrib import admin
from .models import CustomComment

class CustomCommentAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'user_full_name', 'is_removed', )
    list_filter = ('is_removed', )
    search_fields = ('user__first_name', 'user__last_name', 'user__email', )

    def user_full_name(self, obj):
        return obj.user.get_full_name()
    user_full_name.short_description = 'user'

admin.site.register(CustomComment, CustomCommentAdmin)
