from django.contrib import admin
from .models import SocialProject, TaskGroup, Task, SocialForumTopic, SocialForumEntry


class FullUserNameMixin(object):
    def get_full_username(self, obj):
        return obj.creator.profile
    get_full_username.short_description = 'user'


class SocialProjectAdmin(admin.ModelAdmin, FullUserNameMixin):
    list_display = ('name', 'location', 'get_full_username', 'is_done',)
    readonly_fields = ('slug',)


class TaskInlineAdmin(admin.TabularInline):
    model = Task
    extra = 1


class TaskGroupAdmin(admin.ModelAdmin, FullUserNameMixin):
    list_display = ('name', 'project', 'get_full_username',)
    inlines = (TaskInlineAdmin,)
    search_fields = ('creator__first_name', 'creator__last_name',
                     'creator__email', 'name', 'project__name',)


class SocialForumTopicAdmin(admin.ModelAdmin, FullUserNameMixin):
    list_display = ('name', 'get_full_username', 'project',)
    readonly_fields = ('slug',)
    list_filter = ('date_created',)
    search_fields = ('creator__first_name', 'creator__last_name',
                     'creator__email', 'name', 'project__name',)


class SocialForumEntryAdmin(admin.ModelAdmin, FullUserNameMixin):
    list_display = ('get_full_username', 'topic', 'project_name',)
    search_fields = ('creator__first_name', 'creator__last_name',
                     'creator__email', 'topic__name',)

    def project_name(self, obj):
        return obj.topic.project
    project_name.short_description = 'project'


admin.site.register(SocialProject, SocialProjectAdmin)
admin.site.register(TaskGroup, TaskGroupAdmin)
admin.site.register(SocialForumTopic, SocialForumTopicAdmin)
admin.site.register(SocialForumEntry, SocialForumEntryAdmin)
