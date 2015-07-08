# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0006_imagelicense'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagelicense',
            name='description_de',
            field=models.TextField(null=True, verbose_name='description', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='imagelicense',
            name='description_en',
            field=models.TextField(null=True, verbose_name='description', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='imagelicense',
            name='description_es',
            field=models.TextField(null=True, verbose_name='description', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='imagelicense',
            name='description_fr',
            field=models.TextField(null=True, verbose_name='description', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='imagelicense',
            name='description_pl',
            field=models.TextField(null=True, verbose_name='description', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='imagelicense',
            name='description_pt',
            field=models.TextField(null=True, verbose_name='description', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='imagelicense',
            name='name_de',
            field=models.CharField(max_length=128, null=True, verbose_name='name'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='imagelicense',
            name='name_en',
            field=models.CharField(max_length=128, null=True, verbose_name='name'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='imagelicense',
            name='name_es',
            field=models.CharField(max_length=128, null=True, verbose_name='name'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='imagelicense',
            name='name_fr',
            field=models.CharField(max_length=128, null=True, verbose_name='name'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='imagelicense',
            name='name_pl',
            field=models.CharField(max_length=128, null=True, verbose_name='name'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='imagelicense',
            name='name_pt',
            field=models.CharField(max_length=128, null=True, verbose_name='name'),
            preserve_default=True,
        ),
    ]
