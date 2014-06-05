# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Category.name_af'
        db.add_column(u'ideas_category', 'name_af',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_ar'
        db.add_column(u'ideas_category', 'name_ar',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_az'
        db.add_column(u'ideas_category', 'name_az',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_bg'
        db.add_column(u'ideas_category', 'name_bg',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_be'
        db.add_column(u'ideas_category', 'name_be',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_bn'
        db.add_column(u'ideas_category', 'name_bn',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_br'
        db.add_column(u'ideas_category', 'name_br',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_bs'
        db.add_column(u'ideas_category', 'name_bs',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_ca'
        db.add_column(u'ideas_category', 'name_ca',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_cs'
        db.add_column(u'ideas_category', 'name_cs',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_cy'
        db.add_column(u'ideas_category', 'name_cy',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_da'
        db.add_column(u'ideas_category', 'name_da',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_de'
        db.add_column(u'ideas_category', 'name_de',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_el'
        db.add_column(u'ideas_category', 'name_el',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_en'
        db.add_column(u'ideas_category', 'name_en',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_en_gb'
        db.add_column(u'ideas_category', 'name_en_gb',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_eo'
        db.add_column(u'ideas_category', 'name_eo',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_es'
        db.add_column(u'ideas_category', 'name_es',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_es_ar'
        db.add_column(u'ideas_category', 'name_es_ar',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_es_mx'
        db.add_column(u'ideas_category', 'name_es_mx',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_es_ni'
        db.add_column(u'ideas_category', 'name_es_ni',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_es_ve'
        db.add_column(u'ideas_category', 'name_es_ve',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_et'
        db.add_column(u'ideas_category', 'name_et',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_eu'
        db.add_column(u'ideas_category', 'name_eu',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_fa'
        db.add_column(u'ideas_category', 'name_fa',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_fi'
        db.add_column(u'ideas_category', 'name_fi',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_fr'
        db.add_column(u'ideas_category', 'name_fr',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_fy_nl'
        db.add_column(u'ideas_category', 'name_fy_nl',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_ga'
        db.add_column(u'ideas_category', 'name_ga',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_gl'
        db.add_column(u'ideas_category', 'name_gl',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_he'
        db.add_column(u'ideas_category', 'name_he',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_hi'
        db.add_column(u'ideas_category', 'name_hi',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_hr'
        db.add_column(u'ideas_category', 'name_hr',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_hu'
        db.add_column(u'ideas_category', 'name_hu',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_ia'
        db.add_column(u'ideas_category', 'name_ia',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_id'
        db.add_column(u'ideas_category', 'name_id',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_is'
        db.add_column(u'ideas_category', 'name_is',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_it'
        db.add_column(u'ideas_category', 'name_it',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_ja'
        db.add_column(u'ideas_category', 'name_ja',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_ka'
        db.add_column(u'ideas_category', 'name_ka',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_kk'
        db.add_column(u'ideas_category', 'name_kk',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_km'
        db.add_column(u'ideas_category', 'name_km',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_kn'
        db.add_column(u'ideas_category', 'name_kn',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_ko'
        db.add_column(u'ideas_category', 'name_ko',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_lb'
        db.add_column(u'ideas_category', 'name_lb',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_lt'
        db.add_column(u'ideas_category', 'name_lt',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_lv'
        db.add_column(u'ideas_category', 'name_lv',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_mk'
        db.add_column(u'ideas_category', 'name_mk',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_ml'
        db.add_column(u'ideas_category', 'name_ml',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_mn'
        db.add_column(u'ideas_category', 'name_mn',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_my'
        db.add_column(u'ideas_category', 'name_my',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_nb'
        db.add_column(u'ideas_category', 'name_nb',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_ne'
        db.add_column(u'ideas_category', 'name_ne',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_nl'
        db.add_column(u'ideas_category', 'name_nl',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_nn'
        db.add_column(u'ideas_category', 'name_nn',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_os'
        db.add_column(u'ideas_category', 'name_os',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_pa'
        db.add_column(u'ideas_category', 'name_pa',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_pl'
        db.add_column(u'ideas_category', 'name_pl',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_pt'
        db.add_column(u'ideas_category', 'name_pt',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_pt_br'
        db.add_column(u'ideas_category', 'name_pt_br',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_ro'
        db.add_column(u'ideas_category', 'name_ro',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_ru'
        db.add_column(u'ideas_category', 'name_ru',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_sk'
        db.add_column(u'ideas_category', 'name_sk',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_sl'
        db.add_column(u'ideas_category', 'name_sl',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_sq'
        db.add_column(u'ideas_category', 'name_sq',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_sr'
        db.add_column(u'ideas_category', 'name_sr',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_sr_latn'
        db.add_column(u'ideas_category', 'name_sr_latn',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_sv'
        db.add_column(u'ideas_category', 'name_sv',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_sw'
        db.add_column(u'ideas_category', 'name_sw',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_ta'
        db.add_column(u'ideas_category', 'name_ta',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_te'
        db.add_column(u'ideas_category', 'name_te',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_th'
        db.add_column(u'ideas_category', 'name_th',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_tr'
        db.add_column(u'ideas_category', 'name_tr',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_tt'
        db.add_column(u'ideas_category', 'name_tt',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_udm'
        db.add_column(u'ideas_category', 'name_udm',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_uk'
        db.add_column(u'ideas_category', 'name_uk',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_ur'
        db.add_column(u'ideas_category', 'name_ur',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_vi'
        db.add_column(u'ideas_category', 'name_vi',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_zh_cn'
        db.add_column(u'ideas_category', 'name_zh_cn',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_zh_tw'
        db.add_column(u'ideas_category', 'name_zh_tw',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_af'
        db.add_column(u'ideas_category', 'description_af',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_ar'
        db.add_column(u'ideas_category', 'description_ar',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_az'
        db.add_column(u'ideas_category', 'description_az',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_bg'
        db.add_column(u'ideas_category', 'description_bg',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_be'
        db.add_column(u'ideas_category', 'description_be',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_bn'
        db.add_column(u'ideas_category', 'description_bn',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_br'
        db.add_column(u'ideas_category', 'description_br',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_bs'
        db.add_column(u'ideas_category', 'description_bs',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_ca'
        db.add_column(u'ideas_category', 'description_ca',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_cs'
        db.add_column(u'ideas_category', 'description_cs',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_cy'
        db.add_column(u'ideas_category', 'description_cy',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_da'
        db.add_column(u'ideas_category', 'description_da',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_de'
        db.add_column(u'ideas_category', 'description_de',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_el'
        db.add_column(u'ideas_category', 'description_el',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_en'
        db.add_column(u'ideas_category', 'description_en',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_en_gb'
        db.add_column(u'ideas_category', 'description_en_gb',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_eo'
        db.add_column(u'ideas_category', 'description_eo',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_es'
        db.add_column(u'ideas_category', 'description_es',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_es_ar'
        db.add_column(u'ideas_category', 'description_es_ar',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_es_mx'
        db.add_column(u'ideas_category', 'description_es_mx',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_es_ni'
        db.add_column(u'ideas_category', 'description_es_ni',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_es_ve'
        db.add_column(u'ideas_category', 'description_es_ve',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_et'
        db.add_column(u'ideas_category', 'description_et',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_eu'
        db.add_column(u'ideas_category', 'description_eu',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_fa'
        db.add_column(u'ideas_category', 'description_fa',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_fi'
        db.add_column(u'ideas_category', 'description_fi',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_fr'
        db.add_column(u'ideas_category', 'description_fr',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_fy_nl'
        db.add_column(u'ideas_category', 'description_fy_nl',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_ga'
        db.add_column(u'ideas_category', 'description_ga',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_gl'
        db.add_column(u'ideas_category', 'description_gl',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_he'
        db.add_column(u'ideas_category', 'description_he',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_hi'
        db.add_column(u'ideas_category', 'description_hi',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_hr'
        db.add_column(u'ideas_category', 'description_hr',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_hu'
        db.add_column(u'ideas_category', 'description_hu',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_ia'
        db.add_column(u'ideas_category', 'description_ia',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_id'
        db.add_column(u'ideas_category', 'description_id',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_is'
        db.add_column(u'ideas_category', 'description_is',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_it'
        db.add_column(u'ideas_category', 'description_it',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_ja'
        db.add_column(u'ideas_category', 'description_ja',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_ka'
        db.add_column(u'ideas_category', 'description_ka',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_kk'
        db.add_column(u'ideas_category', 'description_kk',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_km'
        db.add_column(u'ideas_category', 'description_km',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_kn'
        db.add_column(u'ideas_category', 'description_kn',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_ko'
        db.add_column(u'ideas_category', 'description_ko',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_lb'
        db.add_column(u'ideas_category', 'description_lb',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_lt'
        db.add_column(u'ideas_category', 'description_lt',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_lv'
        db.add_column(u'ideas_category', 'description_lv',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_mk'
        db.add_column(u'ideas_category', 'description_mk',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_ml'
        db.add_column(u'ideas_category', 'description_ml',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_mn'
        db.add_column(u'ideas_category', 'description_mn',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_my'
        db.add_column(u'ideas_category', 'description_my',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_nb'
        db.add_column(u'ideas_category', 'description_nb',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_ne'
        db.add_column(u'ideas_category', 'description_ne',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_nl'
        db.add_column(u'ideas_category', 'description_nl',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_nn'
        db.add_column(u'ideas_category', 'description_nn',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_os'
        db.add_column(u'ideas_category', 'description_os',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_pa'
        db.add_column(u'ideas_category', 'description_pa',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_pl'
        db.add_column(u'ideas_category', 'description_pl',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_pt'
        db.add_column(u'ideas_category', 'description_pt',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_pt_br'
        db.add_column(u'ideas_category', 'description_pt_br',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_ro'
        db.add_column(u'ideas_category', 'description_ro',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_ru'
        db.add_column(u'ideas_category', 'description_ru',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_sk'
        db.add_column(u'ideas_category', 'description_sk',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_sl'
        db.add_column(u'ideas_category', 'description_sl',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_sq'
        db.add_column(u'ideas_category', 'description_sq',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_sr'
        db.add_column(u'ideas_category', 'description_sr',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_sr_latn'
        db.add_column(u'ideas_category', 'description_sr_latn',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_sv'
        db.add_column(u'ideas_category', 'description_sv',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_sw'
        db.add_column(u'ideas_category', 'description_sw',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_ta'
        db.add_column(u'ideas_category', 'description_ta',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_te'
        db.add_column(u'ideas_category', 'description_te',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_th'
        db.add_column(u'ideas_category', 'description_th',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_tr'
        db.add_column(u'ideas_category', 'description_tr',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_tt'
        db.add_column(u'ideas_category', 'description_tt',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_udm'
        db.add_column(u'ideas_category', 'description_udm',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_uk'
        db.add_column(u'ideas_category', 'description_uk',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_ur'
        db.add_column(u'ideas_category', 'description_ur',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_vi'
        db.add_column(u'ideas_category', 'description_vi',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_zh_cn'
        db.add_column(u'ideas_category', 'description_zh_cn',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_zh_tw'
        db.add_column(u'ideas_category', 'description_zh_tw',
                      self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Category.name_af'
        db.delete_column(u'ideas_category', 'name_af')

        # Deleting field 'Category.name_ar'
        db.delete_column(u'ideas_category', 'name_ar')

        # Deleting field 'Category.name_az'
        db.delete_column(u'ideas_category', 'name_az')

        # Deleting field 'Category.name_bg'
        db.delete_column(u'ideas_category', 'name_bg')

        # Deleting field 'Category.name_be'
        db.delete_column(u'ideas_category', 'name_be')

        # Deleting field 'Category.name_bn'
        db.delete_column(u'ideas_category', 'name_bn')

        # Deleting field 'Category.name_br'
        db.delete_column(u'ideas_category', 'name_br')

        # Deleting field 'Category.name_bs'
        db.delete_column(u'ideas_category', 'name_bs')

        # Deleting field 'Category.name_ca'
        db.delete_column(u'ideas_category', 'name_ca')

        # Deleting field 'Category.name_cs'
        db.delete_column(u'ideas_category', 'name_cs')

        # Deleting field 'Category.name_cy'
        db.delete_column(u'ideas_category', 'name_cy')

        # Deleting field 'Category.name_da'
        db.delete_column(u'ideas_category', 'name_da')

        # Deleting field 'Category.name_de'
        db.delete_column(u'ideas_category', 'name_de')

        # Deleting field 'Category.name_el'
        db.delete_column(u'ideas_category', 'name_el')

        # Deleting field 'Category.name_en'
        db.delete_column(u'ideas_category', 'name_en')

        # Deleting field 'Category.name_en_gb'
        db.delete_column(u'ideas_category', 'name_en_gb')

        # Deleting field 'Category.name_eo'
        db.delete_column(u'ideas_category', 'name_eo')

        # Deleting field 'Category.name_es'
        db.delete_column(u'ideas_category', 'name_es')

        # Deleting field 'Category.name_es_ar'
        db.delete_column(u'ideas_category', 'name_es_ar')

        # Deleting field 'Category.name_es_mx'
        db.delete_column(u'ideas_category', 'name_es_mx')

        # Deleting field 'Category.name_es_ni'
        db.delete_column(u'ideas_category', 'name_es_ni')

        # Deleting field 'Category.name_es_ve'
        db.delete_column(u'ideas_category', 'name_es_ve')

        # Deleting field 'Category.name_et'
        db.delete_column(u'ideas_category', 'name_et')

        # Deleting field 'Category.name_eu'
        db.delete_column(u'ideas_category', 'name_eu')

        # Deleting field 'Category.name_fa'
        db.delete_column(u'ideas_category', 'name_fa')

        # Deleting field 'Category.name_fi'
        db.delete_column(u'ideas_category', 'name_fi')

        # Deleting field 'Category.name_fr'
        db.delete_column(u'ideas_category', 'name_fr')

        # Deleting field 'Category.name_fy_nl'
        db.delete_column(u'ideas_category', 'name_fy_nl')

        # Deleting field 'Category.name_ga'
        db.delete_column(u'ideas_category', 'name_ga')

        # Deleting field 'Category.name_gl'
        db.delete_column(u'ideas_category', 'name_gl')

        # Deleting field 'Category.name_he'
        db.delete_column(u'ideas_category', 'name_he')

        # Deleting field 'Category.name_hi'
        db.delete_column(u'ideas_category', 'name_hi')

        # Deleting field 'Category.name_hr'
        db.delete_column(u'ideas_category', 'name_hr')

        # Deleting field 'Category.name_hu'
        db.delete_column(u'ideas_category', 'name_hu')

        # Deleting field 'Category.name_ia'
        db.delete_column(u'ideas_category', 'name_ia')

        # Deleting field 'Category.name_id'
        db.delete_column(u'ideas_category', 'name_id')

        # Deleting field 'Category.name_is'
        db.delete_column(u'ideas_category', 'name_is')

        # Deleting field 'Category.name_it'
        db.delete_column(u'ideas_category', 'name_it')

        # Deleting field 'Category.name_ja'
        db.delete_column(u'ideas_category', 'name_ja')

        # Deleting field 'Category.name_ka'
        db.delete_column(u'ideas_category', 'name_ka')

        # Deleting field 'Category.name_kk'
        db.delete_column(u'ideas_category', 'name_kk')

        # Deleting field 'Category.name_km'
        db.delete_column(u'ideas_category', 'name_km')

        # Deleting field 'Category.name_kn'
        db.delete_column(u'ideas_category', 'name_kn')

        # Deleting field 'Category.name_ko'
        db.delete_column(u'ideas_category', 'name_ko')

        # Deleting field 'Category.name_lb'
        db.delete_column(u'ideas_category', 'name_lb')

        # Deleting field 'Category.name_lt'
        db.delete_column(u'ideas_category', 'name_lt')

        # Deleting field 'Category.name_lv'
        db.delete_column(u'ideas_category', 'name_lv')

        # Deleting field 'Category.name_mk'
        db.delete_column(u'ideas_category', 'name_mk')

        # Deleting field 'Category.name_ml'
        db.delete_column(u'ideas_category', 'name_ml')

        # Deleting field 'Category.name_mn'
        db.delete_column(u'ideas_category', 'name_mn')

        # Deleting field 'Category.name_my'
        db.delete_column(u'ideas_category', 'name_my')

        # Deleting field 'Category.name_nb'
        db.delete_column(u'ideas_category', 'name_nb')

        # Deleting field 'Category.name_ne'
        db.delete_column(u'ideas_category', 'name_ne')

        # Deleting field 'Category.name_nl'
        db.delete_column(u'ideas_category', 'name_nl')

        # Deleting field 'Category.name_nn'
        db.delete_column(u'ideas_category', 'name_nn')

        # Deleting field 'Category.name_os'
        db.delete_column(u'ideas_category', 'name_os')

        # Deleting field 'Category.name_pa'
        db.delete_column(u'ideas_category', 'name_pa')

        # Deleting field 'Category.name_pl'
        db.delete_column(u'ideas_category', 'name_pl')

        # Deleting field 'Category.name_pt'
        db.delete_column(u'ideas_category', 'name_pt')

        # Deleting field 'Category.name_pt_br'
        db.delete_column(u'ideas_category', 'name_pt_br')

        # Deleting field 'Category.name_ro'
        db.delete_column(u'ideas_category', 'name_ro')

        # Deleting field 'Category.name_ru'
        db.delete_column(u'ideas_category', 'name_ru')

        # Deleting field 'Category.name_sk'
        db.delete_column(u'ideas_category', 'name_sk')

        # Deleting field 'Category.name_sl'
        db.delete_column(u'ideas_category', 'name_sl')

        # Deleting field 'Category.name_sq'
        db.delete_column(u'ideas_category', 'name_sq')

        # Deleting field 'Category.name_sr'
        db.delete_column(u'ideas_category', 'name_sr')

        # Deleting field 'Category.name_sr_latn'
        db.delete_column(u'ideas_category', 'name_sr_latn')

        # Deleting field 'Category.name_sv'
        db.delete_column(u'ideas_category', 'name_sv')

        # Deleting field 'Category.name_sw'
        db.delete_column(u'ideas_category', 'name_sw')

        # Deleting field 'Category.name_ta'
        db.delete_column(u'ideas_category', 'name_ta')

        # Deleting field 'Category.name_te'
        db.delete_column(u'ideas_category', 'name_te')

        # Deleting field 'Category.name_th'
        db.delete_column(u'ideas_category', 'name_th')

        # Deleting field 'Category.name_tr'
        db.delete_column(u'ideas_category', 'name_tr')

        # Deleting field 'Category.name_tt'
        db.delete_column(u'ideas_category', 'name_tt')

        # Deleting field 'Category.name_udm'
        db.delete_column(u'ideas_category', 'name_udm')

        # Deleting field 'Category.name_uk'
        db.delete_column(u'ideas_category', 'name_uk')

        # Deleting field 'Category.name_ur'
        db.delete_column(u'ideas_category', 'name_ur')

        # Deleting field 'Category.name_vi'
        db.delete_column(u'ideas_category', 'name_vi')

        # Deleting field 'Category.name_zh_cn'
        db.delete_column(u'ideas_category', 'name_zh_cn')

        # Deleting field 'Category.name_zh_tw'
        db.delete_column(u'ideas_category', 'name_zh_tw')

        # Deleting field 'Category.description_af'
        db.delete_column(u'ideas_category', 'description_af')

        # Deleting field 'Category.description_ar'
        db.delete_column(u'ideas_category', 'description_ar')

        # Deleting field 'Category.description_az'
        db.delete_column(u'ideas_category', 'description_az')

        # Deleting field 'Category.description_bg'
        db.delete_column(u'ideas_category', 'description_bg')

        # Deleting field 'Category.description_be'
        db.delete_column(u'ideas_category', 'description_be')

        # Deleting field 'Category.description_bn'
        db.delete_column(u'ideas_category', 'description_bn')

        # Deleting field 'Category.description_br'
        db.delete_column(u'ideas_category', 'description_br')

        # Deleting field 'Category.description_bs'
        db.delete_column(u'ideas_category', 'description_bs')

        # Deleting field 'Category.description_ca'
        db.delete_column(u'ideas_category', 'description_ca')

        # Deleting field 'Category.description_cs'
        db.delete_column(u'ideas_category', 'description_cs')

        # Deleting field 'Category.description_cy'
        db.delete_column(u'ideas_category', 'description_cy')

        # Deleting field 'Category.description_da'
        db.delete_column(u'ideas_category', 'description_da')

        # Deleting field 'Category.description_de'
        db.delete_column(u'ideas_category', 'description_de')

        # Deleting field 'Category.description_el'
        db.delete_column(u'ideas_category', 'description_el')

        # Deleting field 'Category.description_en'
        db.delete_column(u'ideas_category', 'description_en')

        # Deleting field 'Category.description_en_gb'
        db.delete_column(u'ideas_category', 'description_en_gb')

        # Deleting field 'Category.description_eo'
        db.delete_column(u'ideas_category', 'description_eo')

        # Deleting field 'Category.description_es'
        db.delete_column(u'ideas_category', 'description_es')

        # Deleting field 'Category.description_es_ar'
        db.delete_column(u'ideas_category', 'description_es_ar')

        # Deleting field 'Category.description_es_mx'
        db.delete_column(u'ideas_category', 'description_es_mx')

        # Deleting field 'Category.description_es_ni'
        db.delete_column(u'ideas_category', 'description_es_ni')

        # Deleting field 'Category.description_es_ve'
        db.delete_column(u'ideas_category', 'description_es_ve')

        # Deleting field 'Category.description_et'
        db.delete_column(u'ideas_category', 'description_et')

        # Deleting field 'Category.description_eu'
        db.delete_column(u'ideas_category', 'description_eu')

        # Deleting field 'Category.description_fa'
        db.delete_column(u'ideas_category', 'description_fa')

        # Deleting field 'Category.description_fi'
        db.delete_column(u'ideas_category', 'description_fi')

        # Deleting field 'Category.description_fr'
        db.delete_column(u'ideas_category', 'description_fr')

        # Deleting field 'Category.description_fy_nl'
        db.delete_column(u'ideas_category', 'description_fy_nl')

        # Deleting field 'Category.description_ga'
        db.delete_column(u'ideas_category', 'description_ga')

        # Deleting field 'Category.description_gl'
        db.delete_column(u'ideas_category', 'description_gl')

        # Deleting field 'Category.description_he'
        db.delete_column(u'ideas_category', 'description_he')

        # Deleting field 'Category.description_hi'
        db.delete_column(u'ideas_category', 'description_hi')

        # Deleting field 'Category.description_hr'
        db.delete_column(u'ideas_category', 'description_hr')

        # Deleting field 'Category.description_hu'
        db.delete_column(u'ideas_category', 'description_hu')

        # Deleting field 'Category.description_ia'
        db.delete_column(u'ideas_category', 'description_ia')

        # Deleting field 'Category.description_id'
        db.delete_column(u'ideas_category', 'description_id')

        # Deleting field 'Category.description_is'
        db.delete_column(u'ideas_category', 'description_is')

        # Deleting field 'Category.description_it'
        db.delete_column(u'ideas_category', 'description_it')

        # Deleting field 'Category.description_ja'
        db.delete_column(u'ideas_category', 'description_ja')

        # Deleting field 'Category.description_ka'
        db.delete_column(u'ideas_category', 'description_ka')

        # Deleting field 'Category.description_kk'
        db.delete_column(u'ideas_category', 'description_kk')

        # Deleting field 'Category.description_km'
        db.delete_column(u'ideas_category', 'description_km')

        # Deleting field 'Category.description_kn'
        db.delete_column(u'ideas_category', 'description_kn')

        # Deleting field 'Category.description_ko'
        db.delete_column(u'ideas_category', 'description_ko')

        # Deleting field 'Category.description_lb'
        db.delete_column(u'ideas_category', 'description_lb')

        # Deleting field 'Category.description_lt'
        db.delete_column(u'ideas_category', 'description_lt')

        # Deleting field 'Category.description_lv'
        db.delete_column(u'ideas_category', 'description_lv')

        # Deleting field 'Category.description_mk'
        db.delete_column(u'ideas_category', 'description_mk')

        # Deleting field 'Category.description_ml'
        db.delete_column(u'ideas_category', 'description_ml')

        # Deleting field 'Category.description_mn'
        db.delete_column(u'ideas_category', 'description_mn')

        # Deleting field 'Category.description_my'
        db.delete_column(u'ideas_category', 'description_my')

        # Deleting field 'Category.description_nb'
        db.delete_column(u'ideas_category', 'description_nb')

        # Deleting field 'Category.description_ne'
        db.delete_column(u'ideas_category', 'description_ne')

        # Deleting field 'Category.description_nl'
        db.delete_column(u'ideas_category', 'description_nl')

        # Deleting field 'Category.description_nn'
        db.delete_column(u'ideas_category', 'description_nn')

        # Deleting field 'Category.description_os'
        db.delete_column(u'ideas_category', 'description_os')

        # Deleting field 'Category.description_pa'
        db.delete_column(u'ideas_category', 'description_pa')

        # Deleting field 'Category.description_pl'
        db.delete_column(u'ideas_category', 'description_pl')

        # Deleting field 'Category.description_pt'
        db.delete_column(u'ideas_category', 'description_pt')

        # Deleting field 'Category.description_pt_br'
        db.delete_column(u'ideas_category', 'description_pt_br')

        # Deleting field 'Category.description_ro'
        db.delete_column(u'ideas_category', 'description_ro')

        # Deleting field 'Category.description_ru'
        db.delete_column(u'ideas_category', 'description_ru')

        # Deleting field 'Category.description_sk'
        db.delete_column(u'ideas_category', 'description_sk')

        # Deleting field 'Category.description_sl'
        db.delete_column(u'ideas_category', 'description_sl')

        # Deleting field 'Category.description_sq'
        db.delete_column(u'ideas_category', 'description_sq')

        # Deleting field 'Category.description_sr'
        db.delete_column(u'ideas_category', 'description_sr')

        # Deleting field 'Category.description_sr_latn'
        db.delete_column(u'ideas_category', 'description_sr_latn')

        # Deleting field 'Category.description_sv'
        db.delete_column(u'ideas_category', 'description_sv')

        # Deleting field 'Category.description_sw'
        db.delete_column(u'ideas_category', 'description_sw')

        # Deleting field 'Category.description_ta'
        db.delete_column(u'ideas_category', 'description_ta')

        # Deleting field 'Category.description_te'
        db.delete_column(u'ideas_category', 'description_te')

        # Deleting field 'Category.description_th'
        db.delete_column(u'ideas_category', 'description_th')

        # Deleting field 'Category.description_tr'
        db.delete_column(u'ideas_category', 'description_tr')

        # Deleting field 'Category.description_tt'
        db.delete_column(u'ideas_category', 'description_tt')

        # Deleting field 'Category.description_udm'
        db.delete_column(u'ideas_category', 'description_udm')

        # Deleting field 'Category.description_uk'
        db.delete_column(u'ideas_category', 'description_uk')

        # Deleting field 'Category.description_ur'
        db.delete_column(u'ideas_category', 'description_ur')

        # Deleting field 'Category.description_vi'
        db.delete_column(u'ideas_category', 'description_vi')

        # Deleting field 'Category.description_zh_cn'
        db.delete_column(u'ideas_category', 'description_zh_cn')

        # Deleting field 'Category.description_zh_tw'
        db.delete_column(u'ideas_category', 'description_zh_tw')


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
        u'ideas.category': {
            'Meta': {'object_name': 'Category'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '1024'}),
            'description_af': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_ar': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_az': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_be': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_bg': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_bn': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_br': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_bs': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_ca': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_cs': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_cy': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_da': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_de': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_el': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_en': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_en_gb': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_eo': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_es': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_es_ar': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_es_mx': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_es_ni': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_es_ve': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_et': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_eu': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_fa': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_fi': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_fr': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_fy_nl': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_ga': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_gl': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_he': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_hi': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_hr': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_hu': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_ia': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_id': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_is': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_it': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_ja': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_ka': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_kk': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_km': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_kn': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_ko': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_lb': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_lt': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_lv': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_mk': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_ml': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_mn': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_my': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_nb': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_ne': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_nl': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_nn': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_os': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_pa': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_pl': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_pt': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_pt_br': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_ro': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_ru': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_sk': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_sl': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_sq': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_sr': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_sr_latn': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_sv': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_sw': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_ta': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_te': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_th': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_tr': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_tt': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_udm': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_uk': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_ur': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_vi': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_zh_cn': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'description_zh_tw': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'name_af': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_ar': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_az': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_be': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_bg': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_bn': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_br': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_bs': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_ca': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_cs': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_cy': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_da': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_de': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_el': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_en_gb': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_eo': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_es': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_es_ar': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_es_mx': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_es_ni': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_es_ve': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_et': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_eu': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_fa': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_fi': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_fr': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_fy_nl': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_ga': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_gl': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_he': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_hi': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_hr': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_hu': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_ia': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_is': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_it': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_ja': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_ka': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_kk': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_km': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_kn': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_ko': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_lb': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_lt': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_lv': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_mk': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_ml': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_mn': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_my': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_nb': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_ne': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_nl': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_nn': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_os': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_pa': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_pl': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_pt': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_pt_br': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_ro': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_sk': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_sl': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_sq': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_sr': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_sr_latn': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_sv': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_sw': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_ta': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_te': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_th': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_tr': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_tt': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_udm': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_uk': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_ur': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_vi': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_zh_cn': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'name_zh_tw': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        u'ideas.idea': {
            'Meta': {'object_name': 'Idea'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ideas.Category']", 'null': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'edited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['locations.Location']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '64'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'ideas.vote': {
            'Meta': {'object_name': 'Vote'},
            'date_voted': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idea': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ideas.Idea']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'vote': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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
        }
    }

    complete_apps = ['ideas']