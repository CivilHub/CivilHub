# -*- coding: utf-8 -*-
from django.conf.urls import url

from rest.routers import HybridRouter

import api

router = HybridRouter()
router.register('recommendations', api.BlessViewSet, 'recommendations')
router.add_api_view('bless', url(r'^bless/', api.BlessAPIView.as_view(), name='bless'))
