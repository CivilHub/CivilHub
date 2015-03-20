# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_article_subtitle'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='subtitle_cz',
            field=models.CharField(default='', max_length=200, null=True, verbose_name='subtitle', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='subtitle_de',
            field=models.CharField(default='', max_length=200, null=True, verbose_name='subtitle', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='subtitle_en',
            field=models.CharField(default='', max_length=200, null=True, verbose_name='subtitle', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='subtitle_es',
            field=models.CharField(default='', max_length=200, null=True, verbose_name='subtitle', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='subtitle_fr',
            field=models.CharField(default='', max_length=200, null=True, verbose_name='subtitle', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='subtitle_it',
            field=models.CharField(default='', max_length=200, null=True, verbose_name='subtitle', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='subtitle_pl',
            field=models.CharField(default='', max_length=200, null=True, verbose_name='subtitle', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='subtitle_pt',
            field=models.CharField(default='', max_length=200, null=True, verbose_name='subtitle', blank=True),
            preserve_default=True,
        ),
    ]
