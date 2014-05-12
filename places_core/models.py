from django.db import models
from django.contrib.comments.models import BaseCommentAbstractModel
from django.contrib.auth.models import User

class AbuseReport(BaseCommentAbstractModel):
    """
    Abuse reports to show to admins and moderators. All registered users
    can send reports, but no one except superadmins is allowed to delete
    and edit them.
    """
    sender  = models.ForeignKey(User)
    comment = models.CharField(max_length=2048)
    status  = models.BooleanField(default=False)
    date_reported = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
