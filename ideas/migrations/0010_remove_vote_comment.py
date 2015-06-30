# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0009_vote_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='comment',
        ),
    ]
