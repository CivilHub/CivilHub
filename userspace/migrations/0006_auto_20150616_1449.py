# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('userspace', '0005_closeaccountdemand'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='closeaccountdemand',
            options={'verbose_name': 'close account demand', 'verbose_name_plural': 'close account demands'},
        ),
        migrations.AlterField(
            model_name='closeaccountdemand',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True),
            preserve_default=True,
        ),
    ]
