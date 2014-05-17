# -*- coding: utf-8 -*-
from django.db import models
from annoying.fields import AutoOneToOneField
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = AutoOneToOneField(User, primary_key=True, related_name='profile')
    birth_date = models.CharField(max_length=10, blank=True)
    activation_link = models.CharField(max_length=1024)
    avatar = models.ImageField(
        upload_to = "img/avatars/",
        default = 'img/avatars/anonymous.png'
    )
