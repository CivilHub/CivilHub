# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import organizations.models
import locations.models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_socialproject_authors_group'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('locations', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, verbose_name='name')),
                ('name_en', models.CharField(max_length=64, null=True, verbose_name='name')),
                ('name_pl', models.CharField(max_length=64, null=True, verbose_name='name')),
                ('name_es', models.CharField(max_length=64, null=True, verbose_name='name')),
                ('name_de', models.CharField(max_length=64, null=True, verbose_name='name')),
                ('name_pt', models.CharField(max_length=64, null=True, verbose_name='name')),
                ('name_fr', models.CharField(max_length=64, null=True, verbose_name='name')),
                ('name_it', models.CharField(max_length=64, null=True, verbose_name='name')),
                ('name_cz', models.CharField(max_length=64, null=True, verbose_name='name')),
                ('description', models.TextField(default='', verbose_name='description', blank=True)),
                ('description_en', models.TextField(default='', null=True, verbose_name='description', blank=True)),
                ('description_pl', models.TextField(default='', null=True, verbose_name='description', blank=True)),
                ('description_es', models.TextField(default='', null=True, verbose_name='description', blank=True)),
                ('description_de', models.TextField(default='', null=True, verbose_name='description', blank=True)),
                ('description_pt', models.TextField(default='', null=True, verbose_name='description', blank=True)),
                ('description_fr', models.TextField(default='', null=True, verbose_name='description', blank=True)),
                ('description_it', models.TextField(default='', null=True, verbose_name='description', blank=True)),
                ('description_cz', models.TextField(default='', null=True, verbose_name='description', blank=True)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(unique=True, max_length=255, verbose_name='key', blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('date_accepted', models.DateTimeField(null=True, verbose_name='date accepted', blank=True)),
                ('is_accepted', models.BooleanField(default=False, verbose_name='is accepted')),
            ],
            options={
                'verbose_name': 'invitation',
                'verbose_name_plural': 'invitations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('slug', models.CharField(max_length=210, verbose_name='slug')),
                ('description', models.TextField(default='', verbose_name='description', blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='date modified')),
                ('krs', models.CharField(default='', max_length=255, verbose_name='KRS', blank=True)),
                ('email', models.EmailField(max_length=75, null=True, verbose_name='contact mail', blank=True)),
                ('website', models.URLField(null=True, verbose_name='website', blank=True)),
                ('logo', models.ImageField(default='img/ngo/default.jpg', upload_to=organizations.models.logo_upload_path)),
                ('verified', models.BooleanField(default=False, verbose_name='is verified')),
                ('image', models.ImageField(default='img/organizations/default.jpg', upload_to=organizations.models.background_upload_path, verbose_name='background image')),
                ('category', models.ForeignKey(verbose_name='category', blank=True, to='organizations.Category', null=True)),
                ('creator', models.ForeignKey(related_name='created_organizations', verbose_name='creator', to=settings.AUTH_USER_MODEL)),
                ('locations', models.ManyToManyField(related_name='organizations', null=True, verbose_name='locations', to='locations.Location', blank=True)),
                ('projects', models.ManyToManyField(related_name='mentors', null=True, to='projects.SocialProject', blank=True)),
                ('users', models.ManyToManyField(related_name='organizations', null=True, verbose_name='members', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'verbose_name': 'organization',
                'verbose_name_plural': 'organizations',
            },
            bases=(models.Model, locations.models.BackgroundModelMixin),
        ),
        migrations.AddField(
            model_name='invitation',
            name='organization',
            field=models.ForeignKey(related_name='invitations', verbose_name='organization', to='organizations.Organization'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='invitation',
            name='user',
            field=models.ForeignKey(related_name='ngo_invitations', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='invitation',
            unique_together=set([('user', 'organization')]),
        ),
    ]
