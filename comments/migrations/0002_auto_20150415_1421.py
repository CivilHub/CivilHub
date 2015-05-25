# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='commentvote',
            options={'verbose_name': 'comment vote', 'verbose_name_plural': 'comment votes'},
        ),
        migrations.AlterModelOptions(
            name='customcomment',
            options={'verbose_name': 'comment', 'verbose_name_plural': 'comments'},
        ),
        migrations.AlterUniqueTogether(
            name='commentvote',
            unique_together=set([('user', 'comment')]),
        ),
    ]
