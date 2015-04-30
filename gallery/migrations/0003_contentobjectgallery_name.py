# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0002_contentobjectgallery_contentobjectpicture'),
    ]

    operations = [
        migrations.AddField(
            model_name='contentobjectgallery',
            name='name',
            field=models.CharField(default='', max_length=64, blank=True),
            preserve_default=True,
        ),
    ]
