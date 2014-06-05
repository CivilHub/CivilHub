# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Badge', fields ['name_zh_tw']
        db.create_unique(u'userspace_badge', ['name_zh_tw'])

        # Adding unique constraint on 'Badge', fields ['name_es_ar']
        db.create_unique(u'userspace_badge', ['name_es_ar'])

        # Adding unique constraint on 'Badge', fields ['name_udm']
        db.create_unique(u'userspace_badge', ['name_udm'])

        # Adding unique constraint on 'Badge', fields ['name_ia']
        db.create_unique(u'userspace_badge', ['name_ia'])

        # Adding unique constraint on 'Badge', fields ['name_de']
        db.create_unique(u'userspace_badge', ['name_de'])

        # Adding unique constraint on 'Badge', fields ['name_da']
        db.create_unique(u'userspace_badge', ['name_da'])

        # Adding unique constraint on 'Badge', fields ['name_zh_cn']
        db.create_unique(u'userspace_badge', ['name_zh_cn'])

        # Adding unique constraint on 'Badge', fields ['name_te']
        db.create_unique(u'userspace_badge', ['name_te'])

        # Adding unique constraint on 'Badge', fields ['name_ca']
        db.create_unique(u'userspace_badge', ['name_ca'])

        # Adding unique constraint on 'Badge', fields ['name_ta']
        db.create_unique(u'userspace_badge', ['name_ta'])

        # Adding unique constraint on 'Badge', fields ['name_th']
        db.create_unique(u'userspace_badge', ['name_th'])

        # Adding unique constraint on 'Badge', fields ['name_cs']
        db.create_unique(u'userspace_badge', ['name_cs'])

        # Adding unique constraint on 'Badge', fields ['name_tt']
        db.create_unique(u'userspace_badge', ['name_tt'])

        # Adding unique constraint on 'Badge', fields ['name_kn']
        db.create_unique(u'userspace_badge', ['name_kn'])

        # Adding unique constraint on 'Badge', fields ['name_km']
        db.create_unique(u'userspace_badge', ['name_km'])

        # Adding unique constraint on 'Badge', fields ['name_cy']
        db.create_unique(u'userspace_badge', ['name_cy'])

        # Adding unique constraint on 'Badge', fields ['name_gl']
        db.create_unique(u'userspace_badge', ['name_gl'])

        # Adding unique constraint on 'Badge', fields ['name_be']
        db.create_unique(u'userspace_badge', ['name_be'])

        # Adding unique constraint on 'Badge', fields ['name']
        db.create_unique(u'userspace_badge', ['name'])

        # Adding unique constraint on 'Badge', fields ['name_sr']
        db.create_unique(u'userspace_badge', ['name_sr'])

        # Adding unique constraint on 'Badge', fields ['name_bg']
        db.create_unique(u'userspace_badge', ['name_bg'])

        # Adding unique constraint on 'Badge', fields ['name_sq']
        db.create_unique(u'userspace_badge', ['name_sq'])

        # Adding unique constraint on 'Badge', fields ['name_sv']
        db.create_unique(u'userspace_badge', ['name_sv'])

        # Adding unique constraint on 'Badge', fields ['name_sw']
        db.create_unique(u'userspace_badge', ['name_sw'])

        # Adding unique constraint on 'Badge', fields ['name_bn']
        db.create_unique(u'userspace_badge', ['name_bn'])

        # Adding unique constraint on 'Badge', fields ['name_es_ve']
        db.create_unique(u'userspace_badge', ['name_es_ve'])

        # Adding unique constraint on 'Badge', fields ['name_ar']
        db.create_unique(u'userspace_badge', ['name_ar'])

        # Adding unique constraint on 'Badge', fields ['name_br']
        db.create_unique(u'userspace_badge', ['name_br'])

        # Adding unique constraint on 'Badge', fields ['name_sk']
        db.create_unique(u'userspace_badge', ['name_sk'])

        # Adding unique constraint on 'Badge', fields ['name_es_ni']
        db.create_unique(u'userspace_badge', ['name_es_ni'])

        # Adding unique constraint on 'Badge', fields ['name_ja']
        db.create_unique(u'userspace_badge', ['name_ja'])

        # Adding unique constraint on 'Badge', fields ['name_sl']
        db.create_unique(u'userspace_badge', ['name_sl'])

        # Adding unique constraint on 'Badge', fields ['name_fr']
        db.create_unique(u'userspace_badge', ['name_fr'])

        # Adding unique constraint on 'Badge', fields ['name_fa']
        db.create_unique(u'userspace_badge', ['name_fa'])

        # Adding unique constraint on 'Badge', fields ['name_fi']
        db.create_unique(u'userspace_badge', ['name_fi'])

        # Adding unique constraint on 'Badge', fields ['name_ml']
        db.create_unique(u'userspace_badge', ['name_ml'])

        # Adding unique constraint on 'Badge', fields ['name_mn']
        db.create_unique(u'userspace_badge', ['name_mn'])

        # Adding unique constraint on 'Badge', fields ['name_mk']
        db.create_unique(u'userspace_badge', ['name_mk'])

        # Adding unique constraint on 'Badge', fields ['name_vi']
        db.create_unique(u'userspace_badge', ['name_vi'])

        # Adding unique constraint on 'Badge', fields ['name_sr_latn']
        db.create_unique(u'userspace_badge', ['name_sr_latn'])

        # Adding unique constraint on 'Badge', fields ['name_my']
        db.create_unique(u'userspace_badge', ['name_my'])

        # Adding unique constraint on 'Badge', fields ['name_et']
        db.create_unique(u'userspace_badge', ['name_et'])

        # Adding unique constraint on 'Badge', fields ['name_eu']
        db.create_unique(u'userspace_badge', ['name_eu'])

        # Adding unique constraint on 'Badge', fields ['name_bs']
        db.create_unique(u'userspace_badge', ['name_bs'])

        # Adding unique constraint on 'Badge', fields ['name_es']
        db.create_unique(u'userspace_badge', ['name_es'])

        # Adding unique constraint on 'Badge', fields ['name_es_mx']
        db.create_unique(u'userspace_badge', ['name_es_mx'])

        # Adding unique constraint on 'Badge', fields ['name_en_gb']
        db.create_unique(u'userspace_badge', ['name_en_gb'])

        # Adding unique constraint on 'Badge', fields ['name_el']
        db.create_unique(u'userspace_badge', ['name_el'])

        # Adding unique constraint on 'Badge', fields ['name_en']
        db.create_unique(u'userspace_badge', ['name_en'])

        # Adding unique constraint on 'Badge', fields ['name_eo']
        db.create_unique(u'userspace_badge', ['name_eo'])

        # Adding unique constraint on 'Badge', fields ['name_lb']
        db.create_unique(u'userspace_badge', ['name_lb'])

        # Adding unique constraint on 'Badge', fields ['name_uk']
        db.create_unique(u'userspace_badge', ['name_uk'])

        # Adding unique constraint on 'Badge', fields ['name_ka']
        db.create_unique(u'userspace_badge', ['name_ka'])

        # Adding unique constraint on 'Badge', fields ['name_lv']
        db.create_unique(u'userspace_badge', ['name_lv'])

        # Adding unique constraint on 'Badge', fields ['name_lt']
        db.create_unique(u'userspace_badge', ['name_lt'])

        # Adding unique constraint on 'Badge', fields ['name_fy_nl']
        db.create_unique(u'userspace_badge', ['name_fy_nl'])

        # Adding unique constraint on 'Badge', fields ['name_os']
        db.create_unique(u'userspace_badge', ['name_os'])

        # Adding unique constraint on 'Badge', fields ['name_pl']
        db.create_unique(u'userspace_badge', ['name_pl'])

        # Adding unique constraint on 'Badge', fields ['name_pa']
        db.create_unique(u'userspace_badge', ['name_pa'])

        # Adding unique constraint on 'Badge', fields ['name_kk']
        db.create_unique(u'userspace_badge', ['name_kk'])

        # Adding unique constraint on 'Badge', fields ['name_ko']
        db.create_unique(u'userspace_badge', ['name_ko'])

        # Adding unique constraint on 'Badge', fields ['name_ga']
        db.create_unique(u'userspace_badge', ['name_ga'])

        # Adding unique constraint on 'Badge', fields ['name_nl']
        db.create_unique(u'userspace_badge', ['name_nl'])

        # Adding unique constraint on 'Badge', fields ['name_nn']
        db.create_unique(u'userspace_badge', ['name_nn'])

        # Adding unique constraint on 'Badge', fields ['name_nb']
        db.create_unique(u'userspace_badge', ['name_nb'])

        # Adding unique constraint on 'Badge', fields ['name_ne']
        db.create_unique(u'userspace_badge', ['name_ne'])

        # Adding unique constraint on 'Badge', fields ['name_pt_br']
        db.create_unique(u'userspace_badge', ['name_pt_br'])

        # Adding unique constraint on 'Badge', fields ['name_pt']
        db.create_unique(u'userspace_badge', ['name_pt'])

        # Adding unique constraint on 'Badge', fields ['name_tr']
        db.create_unique(u'userspace_badge', ['name_tr'])

        # Adding unique constraint on 'Badge', fields ['name_ru']
        db.create_unique(u'userspace_badge', ['name_ru'])

        # Adding unique constraint on 'Badge', fields ['name_is']
        db.create_unique(u'userspace_badge', ['name_is'])

        # Adding unique constraint on 'Badge', fields ['name_it']
        db.create_unique(u'userspace_badge', ['name_it'])

        # Adding unique constraint on 'Badge', fields ['name_id']
        db.create_unique(u'userspace_badge', ['name_id'])

        # Adding unique constraint on 'Badge', fields ['name_ro']
        db.create_unique(u'userspace_badge', ['name_ro'])

        # Adding unique constraint on 'Badge', fields ['name_az']
        db.create_unique(u'userspace_badge', ['name_az'])

        # Adding unique constraint on 'Badge', fields ['name_ur']
        db.create_unique(u'userspace_badge', ['name_ur'])

        # Adding unique constraint on 'Badge', fields ['name_af']
        db.create_unique(u'userspace_badge', ['name_af'])

        # Adding unique constraint on 'Badge', fields ['name_hr']
        db.create_unique(u'userspace_badge', ['name_hr'])

        # Adding unique constraint on 'Badge', fields ['name_hu']
        db.create_unique(u'userspace_badge', ['name_hu'])

        # Adding unique constraint on 'Badge', fields ['name_he']
        db.create_unique(u'userspace_badge', ['name_he'])

        # Adding unique constraint on 'Badge', fields ['name_hi']
        db.create_unique(u'userspace_badge', ['name_hi'])


    def backwards(self, orm):
        # Removing unique constraint on 'Badge', fields ['name_hi']
        db.delete_unique(u'userspace_badge', ['name_hi'])

        # Removing unique constraint on 'Badge', fields ['name_he']
        db.delete_unique(u'userspace_badge', ['name_he'])

        # Removing unique constraint on 'Badge', fields ['name_hu']
        db.delete_unique(u'userspace_badge', ['name_hu'])

        # Removing unique constraint on 'Badge', fields ['name_hr']
        db.delete_unique(u'userspace_badge', ['name_hr'])

        # Removing unique constraint on 'Badge', fields ['name_af']
        db.delete_unique(u'userspace_badge', ['name_af'])

        # Removing unique constraint on 'Badge', fields ['name_ur']
        db.delete_unique(u'userspace_badge', ['name_ur'])

        # Removing unique constraint on 'Badge', fields ['name_az']
        db.delete_unique(u'userspace_badge', ['name_az'])

        # Removing unique constraint on 'Badge', fields ['name_ro']
        db.delete_unique(u'userspace_badge', ['name_ro'])

        # Removing unique constraint on 'Badge', fields ['name_id']
        db.delete_unique(u'userspace_badge', ['name_id'])

        # Removing unique constraint on 'Badge', fields ['name_it']
        db.delete_unique(u'userspace_badge', ['name_it'])

        # Removing unique constraint on 'Badge', fields ['name_is']
        db.delete_unique(u'userspace_badge', ['name_is'])

        # Removing unique constraint on 'Badge', fields ['name_ru']
        db.delete_unique(u'userspace_badge', ['name_ru'])

        # Removing unique constraint on 'Badge', fields ['name_tr']
        db.delete_unique(u'userspace_badge', ['name_tr'])

        # Removing unique constraint on 'Badge', fields ['name_pt']
        db.delete_unique(u'userspace_badge', ['name_pt'])

        # Removing unique constraint on 'Badge', fields ['name_pt_br']
        db.delete_unique(u'userspace_badge', ['name_pt_br'])

        # Removing unique constraint on 'Badge', fields ['name_ne']
        db.delete_unique(u'userspace_badge', ['name_ne'])

        # Removing unique constraint on 'Badge', fields ['name_nb']
        db.delete_unique(u'userspace_badge', ['name_nb'])

        # Removing unique constraint on 'Badge', fields ['name_nn']
        db.delete_unique(u'userspace_badge', ['name_nn'])

        # Removing unique constraint on 'Badge', fields ['name_nl']
        db.delete_unique(u'userspace_badge', ['name_nl'])

        # Removing unique constraint on 'Badge', fields ['name_ga']
        db.delete_unique(u'userspace_badge', ['name_ga'])

        # Removing unique constraint on 'Badge', fields ['name_ko']
        db.delete_unique(u'userspace_badge', ['name_ko'])

        # Removing unique constraint on 'Badge', fields ['name_kk']
        db.delete_unique(u'userspace_badge', ['name_kk'])

        # Removing unique constraint on 'Badge', fields ['name_pa']
        db.delete_unique(u'userspace_badge', ['name_pa'])

        # Removing unique constraint on 'Badge', fields ['name_pl']
        db.delete_unique(u'userspace_badge', ['name_pl'])

        # Removing unique constraint on 'Badge', fields ['name_os']
        db.delete_unique(u'userspace_badge', ['name_os'])

        # Removing unique constraint on 'Badge', fields ['name_fy_nl']
        db.delete_unique(u'userspace_badge', ['name_fy_nl'])

        # Removing unique constraint on 'Badge', fields ['name_lt']
        db.delete_unique(u'userspace_badge', ['name_lt'])

        # Removing unique constraint on 'Badge', fields ['name_lv']
        db.delete_unique(u'userspace_badge', ['name_lv'])

        # Removing unique constraint on 'Badge', fields ['name_ka']
        db.delete_unique(u'userspace_badge', ['name_ka'])

        # Removing unique constraint on 'Badge', fields ['name_uk']
        db.delete_unique(u'userspace_badge', ['name_uk'])

        # Removing unique constraint on 'Badge', fields ['name_lb']
        db.delete_unique(u'userspace_badge', ['name_lb'])

        # Removing unique constraint on 'Badge', fields ['name_eo']
        db.delete_unique(u'userspace_badge', ['name_eo'])

        # Removing unique constraint on 'Badge', fields ['name_en']
        db.delete_unique(u'userspace_badge', ['name_en'])

        # Removing unique constraint on 'Badge', fields ['name_el']
        db.delete_unique(u'userspace_badge', ['name_el'])

        # Removing unique constraint on 'Badge', fields ['name_en_gb']
        db.delete_unique(u'userspace_badge', ['name_en_gb'])

        # Removing unique constraint on 'Badge', fields ['name_es_mx']
        db.delete_unique(u'userspace_badge', ['name_es_mx'])

        # Removing unique constraint on 'Badge', fields ['name_es']
        db.delete_unique(u'userspace_badge', ['name_es'])

        # Removing unique constraint on 'Badge', fields ['name_bs']
        db.delete_unique(u'userspace_badge', ['name_bs'])

        # Removing unique constraint on 'Badge', fields ['name_eu']
        db.delete_unique(u'userspace_badge', ['name_eu'])

        # Removing unique constraint on 'Badge', fields ['name_et']
        db.delete_unique(u'userspace_badge', ['name_et'])

        # Removing unique constraint on 'Badge', fields ['name_my']
        db.delete_unique(u'userspace_badge', ['name_my'])

        # Removing unique constraint on 'Badge', fields ['name_sr_latn']
        db.delete_unique(u'userspace_badge', ['name_sr_latn'])

        # Removing unique constraint on 'Badge', fields ['name_vi']
        db.delete_unique(u'userspace_badge', ['name_vi'])

        # Removing unique constraint on 'Badge', fields ['name_mk']
        db.delete_unique(u'userspace_badge', ['name_mk'])

        # Removing unique constraint on 'Badge', fields ['name_mn']
        db.delete_unique(u'userspace_badge', ['name_mn'])

        # Removing unique constraint on 'Badge', fields ['name_ml']
        db.delete_unique(u'userspace_badge', ['name_ml'])

        # Removing unique constraint on 'Badge', fields ['name_fi']
        db.delete_unique(u'userspace_badge', ['name_fi'])

        # Removing unique constraint on 'Badge', fields ['name_fa']
        db.delete_unique(u'userspace_badge', ['name_fa'])

        # Removing unique constraint on 'Badge', fields ['name_fr']
        db.delete_unique(u'userspace_badge', ['name_fr'])

        # Removing unique constraint on 'Badge', fields ['name_sl']
        db.delete_unique(u'userspace_badge', ['name_sl'])

        # Removing unique constraint on 'Badge', fields ['name_ja']
        db.delete_unique(u'userspace_badge', ['name_ja'])

        # Removing unique constraint on 'Badge', fields ['name_es_ni']
        db.delete_unique(u'userspace_badge', ['name_es_ni'])

        # Removing unique constraint on 'Badge', fields ['name_sk']
        db.delete_unique(u'userspace_badge', ['name_sk'])

        # Removing unique constraint on 'Badge', fields ['name_br']
        db.delete_unique(u'userspace_badge', ['name_br'])

        # Removing unique constraint on 'Badge', fields ['name_ar']
        db.delete_unique(u'userspace_badge', ['name_ar'])

        # Removing unique constraint on 'Badge', fields ['name_es_ve']
        db.delete_unique(u'userspace_badge', ['name_es_ve'])

        # Removing unique constraint on 'Badge', fields ['name_bn']
        db.delete_unique(u'userspace_badge', ['name_bn'])

        # Removing unique constraint on 'Badge', fields ['name_sw']
        db.delete_unique(u'userspace_badge', ['name_sw'])

        # Removing unique constraint on 'Badge', fields ['name_sv']
        db.delete_unique(u'userspace_badge', ['name_sv'])

        # Removing unique constraint on 'Badge', fields ['name_sq']
        db.delete_unique(u'userspace_badge', ['name_sq'])

        # Removing unique constraint on 'Badge', fields ['name_bg']
        db.delete_unique(u'userspace_badge', ['name_bg'])

        # Removing unique constraint on 'Badge', fields ['name_sr']
        db.delete_unique(u'userspace_badge', ['name_sr'])

        # Removing unique constraint on 'Badge', fields ['name']
        db.delete_unique(u'userspace_badge', ['name'])

        # Removing unique constraint on 'Badge', fields ['name_be']
        db.delete_unique(u'userspace_badge', ['name_be'])

        # Removing unique constraint on 'Badge', fields ['name_gl']
        db.delete_unique(u'userspace_badge', ['name_gl'])

        # Removing unique constraint on 'Badge', fields ['name_cy']
        db.delete_unique(u'userspace_badge', ['name_cy'])

        # Removing unique constraint on 'Badge', fields ['name_km']
        db.delete_unique(u'userspace_badge', ['name_km'])

        # Removing unique constraint on 'Badge', fields ['name_kn']
        db.delete_unique(u'userspace_badge', ['name_kn'])

        # Removing unique constraint on 'Badge', fields ['name_tt']
        db.delete_unique(u'userspace_badge', ['name_tt'])

        # Removing unique constraint on 'Badge', fields ['name_cs']
        db.delete_unique(u'userspace_badge', ['name_cs'])

        # Removing unique constraint on 'Badge', fields ['name_th']
        db.delete_unique(u'userspace_badge', ['name_th'])

        # Removing unique constraint on 'Badge', fields ['name_ta']
        db.delete_unique(u'userspace_badge', ['name_ta'])

        # Removing unique constraint on 'Badge', fields ['name_ca']
        db.delete_unique(u'userspace_badge', ['name_ca'])

        # Removing unique constraint on 'Badge', fields ['name_te']
        db.delete_unique(u'userspace_badge', ['name_te'])

        # Removing unique constraint on 'Badge', fields ['name_zh_cn']
        db.delete_unique(u'userspace_badge', ['name_zh_cn'])

        # Removing unique constraint on 'Badge', fields ['name_da']
        db.delete_unique(u'userspace_badge', ['name_da'])

        # Removing unique constraint on 'Badge', fields ['name_de']
        db.delete_unique(u'userspace_badge', ['name_de'])

        # Removing unique constraint on 'Badge', fields ['name_ia']
        db.delete_unique(u'userspace_badge', ['name_ia'])

        # Removing unique constraint on 'Badge', fields ['name_udm']
        db.delete_unique(u'userspace_badge', ['name_udm'])

        # Removing unique constraint on 'Badge', fields ['name_es_ar']
        db.delete_unique(u'userspace_badge', ['name_es_ar'])

        # Removing unique constraint on 'Badge', fields ['name_zh_tw']
        db.delete_unique(u'userspace_badge', ['name_zh_tw'])


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
        u'locations.location': {
            'Meta': {'object_name': 'Location'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'created_locations'", 'blank': 'True', 'to': u"orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '10000', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': "'img/locations/nowhere.jpg'", 'max_length': '100'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['locations.Location']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '64'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'userspace.badge': {
            'Meta': {'object_name': 'Badge'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'description_af': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_ar': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_az': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_be': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_bg': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_bn': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_br': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_bs': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_ca': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_cs': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_cy': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_da': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_de': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_el': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_en_gb': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_eo': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_es_ar': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_es_mx': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_es_ni': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_es_ve': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_et': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_eu': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_fa': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_fi': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_fy_nl': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_ga': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_gl': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_he': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_hi': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_hr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_hu': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_ia': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_id': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_is': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_it': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_ja': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_ka': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_kk': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_km': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_kn': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_ko': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_lb': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_lt': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_lv': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_mk': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_ml': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_mn': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_my': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_nb': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_ne': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_nl': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_nn': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_os': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_pa': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_pl': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_pt': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_pt_br': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_ro': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_ru': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_sk': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_sl': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_sq': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_sr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_sr_latn': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_sv': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_sw': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_ta': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_te': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_th': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_tr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_tt': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_udm': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_uk': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_ur': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_vi': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_zh_cn': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_zh_tw': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'name_af': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_ar': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_az': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_be': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_bg': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_bn': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_br': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_bs': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_ca': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_cs': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_cy': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_da': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_de': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_el': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_en_gb': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_eo': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_es': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_es_ar': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_es_mx': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_es_ni': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_es_ve': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_et': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_eu': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_fa': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_fi': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_fr': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_fy_nl': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_ga': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_gl': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_he': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_hi': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_hr': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_hu': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_ia': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_id': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_is': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_it': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_ja': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_ka': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_kk': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_km': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_kn': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_ko': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_lb': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_lt': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_lv': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_mk': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_ml': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_mn': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_my': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_nb': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_ne': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_nl': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_nn': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_os': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_pa': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_pl': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_pt': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_pt_br': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_ro': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_sk': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_sl': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_sq': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_sr': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_sr_latn': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_sv': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_sw': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_ta': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_te': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_th': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_tr': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_tt': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_udm': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_uk': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_ur': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_vi': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_zh_cn': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_zh_tw': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'default': "'badge.png'", 'max_length': '100'}),
            'user': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'badges'", 'blank': 'True', 'to': u"orm['userspace.UserProfile']"})
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
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'registration'", 'primary_key': 'True', 'to': u"orm['auth.User']"})
        },
        u'userspace.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'avatar': ('django.db.models.fields.files.ImageField', [], {'default': "'img/avatars/anonymous.png'", 'max_length': '100'}),
            'birth_date': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'mod_areas': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'locations'", 'blank': 'True', 'to': u"orm['locations.Location']"}),
            'rank_pts': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'default': "'img/avatars/30x30_anonymous.png'", 'max_length': '100'}),
            'user': ('annoying.fields.AutoOneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['userspace']