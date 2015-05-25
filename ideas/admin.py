# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Idea, Category, Vote

admin.site.register(Idea)
admin.site.register(Category)
admin.site.register(Vote)