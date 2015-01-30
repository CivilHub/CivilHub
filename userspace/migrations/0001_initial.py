# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table(u'userspace_userprofile', (
            ('user', self.gf('annoying.fields.AutoOneToOneField')(related_name='profile', unique=True, primary_key=True, to=orm['auth.User'])),
            ('lang', self.gf('django.db.models.fields.CharField')(default='en', max_length=7)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('rank_pts', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('birth_date', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('clean_username', self.gf('django.db.models.fields.SlugField')(max_length=50, null=True, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('gplus_url', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('fb_url', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('twt_url', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('linkedin_url', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('avatar', self.gf('django.db.models.fields.files.ImageField')(default='img/avatars/anonymous.png', max_length=100)),
            ('thumbnail', self.gf('django.db.models.fields.files.ImageField')(default='img/avatars/30x30_anonymous.png', max_length=100)),
            ('background_image', self.gf('django.db.models.fields.files.ImageField')(default='img/backgrounds/background.jpg', max_length=100)),
        ))
        db.send_create_signal(u'userspace', ['UserProfile'])

        # Adding M2M table for field mod_areas on 'UserProfile'
        m2m_table_name = db.shorten_name(u'userspace_userprofile_mod_areas')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm[u'userspace.userprofile'], null=False)),
            ('location', models.ForeignKey(orm[u'locations.location'], null=False))
        ))
        db.create_unique(m2m_table_name, ['userprofile_id', 'location_id'])

        # Adding model 'Badge'
        db.create_table(u'userspace_badge', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('name_pl', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('name_es', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('name_de', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('name_pt', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('name_fr', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('name_it', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('name_cz', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('description_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('description_pl', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('description_es', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('description_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('description_pt', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('description_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('description_it', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('description_cz', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('thumbnail', self.gf('django.db.models.fields.files.ImageField')(default='img/badges/badge.png', max_length=100)),
        ))
        db.send_create_signal(u'userspace', ['Badge'])

        # Adding M2M table for field user on 'Badge'
        m2m_table_name = db.shorten_name(u'userspace_badge_user')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('badge', models.ForeignKey(orm[u'userspace.badge'], null=False)),
            ('userprofile', models.ForeignKey(orm[u'userspace.userprofile'], null=False))
        ))
        db.create_unique(m2m_table_name, ['badge_id', 'userprofile_id'])

        # Adding model 'RegisterDemand'
        db.create_table(u'userspace_registerdemand', (
            ('activation_link', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=256)),
            ('lang', self.gf('django.db.models.fields.CharField')(default='en', max_length=10)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='registration', primary_key=True, to=orm['auth.User'])),
        ))
        db.send_create_signal(u'userspace', ['RegisterDemand'])

        # Adding model 'LoginData'
        db.create_table(u'userspace_logindata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('address', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
        ))
        db.send_create_signal(u'userspace', ['LoginData'])

        # Adding model 'Bookmark'
        db.create_table(u'userspace_bookmark', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.TextField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'userspace', ['Bookmark'])


    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table(u'userspace_userprofile')

        # Removing M2M table for field mod_areas on 'UserProfile'
        db.delete_table(db.shorten_name(u'userspace_userprofile_mod_areas'))

        # Deleting model 'Badge'
        db.delete_table(u'userspace_badge')

        # Removing M2M table for field user on 'Badge'
        db.delete_table(db.shorten_name(u'userspace_badge_user'))

        # Deleting model 'RegisterDemand'
        db.delete_table(u'userspace_registerdemand')

        # Deleting model 'LoginData'
        db.delete_table(u'userspace_logindata')

        # Deleting model 'Bookmark'
        db.delete_table(u'userspace_bookmark')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'locations.alterlocationname': {
            'Meta': {'object_name': 'AlterLocationName'},
            'altername': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        u'locations.location': {
            'Meta': {'ordering': "['name']", 'object_name': 'Location'},
            'country_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'created_locations'", 'blank': 'True', 'to': u"orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '10000', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': "'img/locations/nowhere.jpg'", 'max_length': '100'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'names': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'alternames'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['locations.AlterLocationName']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['locations.Location']", 'null': 'True', 'blank': 'True'}),
            'population': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '200'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'userspace.badge': {
            'Meta': {'object_name': 'Badge'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'description_cz': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_de': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_it': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_pl': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_pt': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'name_cz': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'name_de': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'name_es': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'name_fr': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'name_it': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'name_pl': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'name_pt': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'default': "'img/badges/badge.png'", 'max_length': '100'}),
            'user': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'badges'", 'blank': 'True', 'to': u"orm['userspace.UserProfile']"})
        },
        u'userspace.bookmark': {
            'Meta': {'object_name': 'Bookmark'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'userspace.logindata': {
            'Meta': {'object_name': 'LoginData'},
            'address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'userspace.registerdemand': {
            'Meta': {'object_name': 'RegisterDemand'},
            'activation_link': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '256'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'lang': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '10'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'registration'", 'primary_key': 'True', 'to': u"orm['auth.User']"})
        },
        u'userspace.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'avatar': ('django.db.models.fields.files.ImageField', [], {'default': "'img/avatars/anonymous.png'", 'max_length': '100'}),
            'background_image': ('django.db.models.fields.files.ImageField', [], {'default': "'img/backgrounds/background.jpg'", 'max_length': '100'}),
            'birth_date': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'clean_username': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fb_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'gplus_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '7'}),
            'linkedin_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'mod_areas': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'locations'", 'blank': 'True', 'to': u"orm['locations.Location']"}),
            'rank_pts': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'default': "'img/avatars/30x30_anonymous.png'", 'max_length': '100'}),
            'twt_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'user': ('annoying.fields.AutoOneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['userspace']