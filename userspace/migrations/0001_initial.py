# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import places_core.storage
import userspace.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('locations', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('thumbnail', models.ImageField(default='img/badges/badge.png', storage=places_core.storage.OverwriteStorage(), upload_to='img/badges')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LoginData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('address', models.IPAddressField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RegisterDemand',
            fields=[
                ('activation_link', models.CharField(max_length=1024)),
                ('ip_address', models.IPAddressField()),
                ('email', models.EmailField(max_length=256)),
                ('lang', models.CharField(default=b'en', max_length=10)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(related_name='registration', primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(related_name='profile', primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('lang', models.CharField(default=b'en', max_length=7, choices=[(b'en', b'English'), (b'pl', b'Polski'), (b'es', b'Espa\xc3\xb1ol (soon)'), (b'de', b'Deutsch'), (b'pt', b'Portugu\xc3\xaas (soon)'), (b'fr', b'Fran\xc3\xa7ais (soon)'), (b'it', b'Italiano (soon)'), (b'cz', b'Ce\xc5\xa1tina (soon)')])),
                ('description', models.TextField(null=True, blank=True)),
                ('rank_pts', models.IntegerField(default=0, blank=True)),
                ('birth_date', models.CharField(max_length=20, null=True, blank=True)),
                ('clean_username', models.SlugField(null=True, blank=True)),
                ('gender', models.CharField(blank=True, max_length=1, null=True, choices=[('M', 'male'), ('F', 'female'), ('U', 'undefined')])),
                ('gplus_url', models.URLField(max_length=255, null=True, verbose_name='Google+ profile url', blank=True)),
                ('fb_url', models.URLField(max_length=255, null=True, verbose_name='Facebook profile url', blank=True)),
                ('twt_url', models.URLField(max_length=255, null=True, verbose_name='Twitter profile url', blank=True)),
                ('linkedin_url', models.URLField(max_length=255, null=True, verbose_name='LinkedIn profile url', blank=True)),
                ('avatar', models.ImageField(default='img/avatars/anonymous.png', storage=places_core.storage.OverwriteStorage(), upload_to='img/avatars/')),
                ('thumbnail', models.ImageField(default='img/avatars/30x30_anonymous.png', storage=places_core.storage.OverwriteStorage(), upload_to='img/avatars/')),
                ('background_image', models.ImageField(default='img/backgrounds/background.jpg', upload_to=userspace.models.get_upload_path)),
                ('mod_areas', models.ManyToManyField(related_name='locations', to='locations.Location', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='logindata',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='badge',
            name='user',
            field=models.ManyToManyField(related_name='badges', to='userspace.UserProfile', blank=True),
            preserve_default=True,
        ),
    ]
