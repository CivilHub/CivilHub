# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userspace', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='badge',
            name='description_cz',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='badge',
            name='description_de',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='badge',
            name='description_en',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='badge',
            name='description_es',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='badge',
            name='description_fr',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='badge',
            name='description_it',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='badge',
            name='description_pl',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='badge',
            name='description_pt',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='badge',
            name='name_cz',
            field=models.CharField(max_length=128, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='badge',
            name='name_de',
            field=models.CharField(max_length=128, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='badge',
            name='name_en',
            field=models.CharField(max_length=128, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='badge',
            name='name_es',
            field=models.CharField(max_length=128, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='badge',
            name='name_fr',
            field=models.CharField(max_length=128, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='badge',
            name='name_it',
            field=models.CharField(max_length=128, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='badge',
            name='name_pl',
            field=models.CharField(max_length=128, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='badge',
            name='name_pt',
            field=models.CharField(max_length=128, null=True),
            preserve_default=True,
        ),
    ]
