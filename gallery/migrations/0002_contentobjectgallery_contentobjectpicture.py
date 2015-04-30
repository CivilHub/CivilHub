# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import gallery.storage


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentObjectGallery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField(null=True, blank=True)),
                ('dirname', models.CharField(max_length=64, blank=True)),
                ('content_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'verbose_name': 'image gallery',
                'verbose_name_plural': 'image galleries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContentObjectPicture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default='', max_length=64, verbose_name='name', blank=True)),
                ('description', models.TextField(default='', verbose_name='description', blank=True)),
                ('image', models.ImageField(upload_to=gallery.storage.upload_path, verbose_name='image')),
                ('date_uploaded', models.DateTimeField(auto_now_add=True, verbose_name='date uploaded')),
                ('gallery', models.ForeignKey(related_name='pictures', verbose_name='gallery', to='gallery.ContentObjectGallery')),
                ('uploaded_by', models.ForeignKey(verbose_name='uploaded by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'picture',
                'verbose_name_plural': 'pictures',
            },
            bases=(models.Model,),
        ),
    ]
