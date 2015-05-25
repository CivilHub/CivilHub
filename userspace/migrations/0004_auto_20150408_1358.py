# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import places_core.storage


class Migration(migrations.Migration):

    dependencies = [
        ('userspace', '0003_auto_20150223_1140'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='logindata',
            options={'ordering': ['-date']},
        ),
        migrations.AddField(
            model_name='userprofile',
            name='website',
            field=models.URLField(max_length=255, null=True, verbose_name='website', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='registerdemand',
            name='lang',
            field=models.CharField(default=b'pl', max_length=10),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(default='img/avatars/anonymous.jpg', storage=places_core.storage.OverwriteStorage(), upload_to='img/avatars/'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='birth_date',
            field=models.CharField(max_length=20, null=True, verbose_name='birth date', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='description',
            field=models.TextField(null=True, verbose_name='about', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(blank=True, max_length=1, null=True, verbose_name='gender', choices=[('M', 'male'), ('F', 'female'), ('U', 'undefined')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='lang',
            field=models.CharField(default=b'pl', max_length=7, verbose_name='language', choices=[(b'en', b'English'), (b'pl', b'Polski'), (b'es', b'Espa\xc3\xb1ol (soon)'), (b'de', b'Deutsch'), (b'pt', b'Portugu\xc3\xaas (soon)'), (b'fr', b'Fran\xc3\xa7ais (soon)'), (b'it', b'Italiano (soon)'), (b'cz', b'Ce\xc5\xa1tina (soon)')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='rank_pts',
            field=models.IntegerField(default=0, verbose_name='points', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='thumbnail',
            field=models.ImageField(default='img/avatars/30x30_anonymous.jpg', storage=places_core.storage.OverwriteStorage(), upload_to='img/avatars/'),
            preserve_default=True,
        ),
    ]
