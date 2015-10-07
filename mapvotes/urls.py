# -*- coding: utf-8 -*-
from rest.routers import HybridRouter

import api

router = HybridRouter()
router.register('markers', api.MarkerViewSet, 'markers')

