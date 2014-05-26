# -*- coding: utf-8 -*-
from django.db import models
from annoying.fields import AutoOneToOneField
from django.contrib.auth.models import User
from places_core.storage import OverwriteStorage


class UserProfile(models.Model):
    """
    Profil użytkownika.
    """
    user = AutoOneToOneField(User, primary_key=True, related_name='profile')
    description = models.TextField(blank=True, null=True)
    birth_date  = models.CharField(max_length=10, blank=True)
    rank_pts = models.IntegerField(blank=True, null=True)
    avatar = models.ImageField(
        upload_to = "img/avatars/",
        default = 'img/avatars/anonymous.png',
        storage = OverwriteStorage()
    )
    thumbnail = models.ImageField(
        upload_to = "img/avatars/",
        default = 'img/avatars/30x30_anonymous.png',
        storage = OverwriteStorage()
    )


class RegisterDemand(models.Model):
    """
    Model przechowujący dane użytkowników zgłaszających chęć rejestracji
    zanim konto zostanie aktywowane.
    TODO: to trzeba później połączyć z cronem i wywalać żądania starsze niż
    określona data.
    """
    activation_link = models.CharField(max_length=1024)
    ip_address = models.IPAddressField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        primary_key=True,
        related_name='registration'
    )


class LoginData(models.Model):
    """
    Tabela przechowująca dane logowania włącznie z nazwą użytkownika,
    adresem IP oraz datą logowania.
    """
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    address = models.IPAddressField()
