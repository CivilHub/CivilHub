# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
