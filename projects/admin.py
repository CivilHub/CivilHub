# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Attachment, \
                    SocialProject, SocialForumTopic, SocialForumEntry, \
                    TaskGroup, Task


class FullUserNameMixin(object):
    def get_full_username(self, obj):
        return obj.creator.profile
    get_full_username.short_description = 'user'


class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'project', 'get_full_username', )
    readonly_fields = ('mime_type', )

    def get_name(self, obj):
        return obj.__unicode__()
    get_name.short_description = 'name'

    def get_full_username(self, obj):
        return obj.uploaded_by.profile
    get_full_username.short_description = 'user'


admin.site.register(Attachment, AttachmentAdmin)


class SocialProjectAdmin(admin.ModelAdmin, FullUserNameMixin):
    list_display = ('name', 'location', 'get_full_username', 'is_done', )
    readonly_fields = ('slug',)
    raw_id_fields = ('location', )


admin.site.register(SocialProject, SocialProjectAdmin)


class TaskInlineAdmin(admin.TabularInline):
    model = Task
    extra = 1


class TaskGroupAdmin(admin.ModelAdmin, FullUserNameMixin):
    list_display = ('name', 'project', 'get_full_username',)
    inlines = (TaskInlineAdmin,)
    search_fields = ('creator__first_name', 'creator__last_name',
                     'creator__email', 'name', 'project__name',)


admin.site.register(TaskGroup, TaskGroupAdmin)


class SocialForumTopicAdmin(admin.ModelAdmin, FullUserNameMixin):
    list_display = ('name', 'get_full_username', 'project',)
    readonly_fields = ('slug',)
    list_filter = ('date_created',)
    search_fields = ('creator__first_name', 'creator__last_name',
                     'creator__email', 'name', 'project__name',)


admin.site.register(SocialForumTopic, SocialForumTopicAdmin)


class SocialForumEntryAdmin(admin.ModelAdmin, FullUserNameMixin):
    list_display = ('get_full_username', 'topic', 'project_name',)
    search_fields = ('creator__first_name', 'creator__last_name',
                     'creator__email', 'topic__name',)

    def project_name(self, obj):
        return obj.topic.project
    project_name.short_description = 'project'


admin.site.register(SocialForumEntry, SocialForumEntryAdmin)
