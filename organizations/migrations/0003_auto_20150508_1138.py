# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_organization_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='creator',
            field=models.ForeignKey(related_name='utworzone_organizacje', verbose_name='creator', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
