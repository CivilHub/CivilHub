from django.contrib import admin
from .models import CustomComment, CommentVote

admin.site.register(CustomComment)
admin.site.register(CommentVote)
