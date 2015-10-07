# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapvotes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='marker',
            name='voting',
            field=models.ForeignKey(related_name='votes', default=1, verbose_name='voting', to='mapvotes.Voting'),
            preserve_default=False,
        ),
    ]
