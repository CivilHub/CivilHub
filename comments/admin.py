from django.contrib import admin
from django.utils.translation import ugettext as _

from .models import CommentVote, CustomComment


class FullNameAdminMixin(admin.ModelAdmin):

    def user_full_name(self, obj):
        return obj.user.get_full_name()
    user_full_name.short_description = _(u'user full name')


class CustomCommentAdmin(FullNameAdminMixin):
    list_display = ('__unicode__', 'user', 'user_full_name',
                    'is_removed', 'submit_date', )
    list_filter = ('is_removed', 'submit_date', )
    search_fields = ('user__first_name', 'user__last_name', 'user__email', )

admin.site.register(CustomComment, CustomCommentAdmin)


class CommentVoteAdmin(FullNameAdminMixin):
    list_display = ('user', 'user_full_name', 'comment',
                    'vote', 'date_voted', )
    list_filter = ('date_voted', )

admin.site.register(CommentVote, CommentVoteAdmin)
