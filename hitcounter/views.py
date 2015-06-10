# -*- coding: utf-8 -*-
import json

from ipware.ip import get_ip

from django.http import HttpResponse

from .decorators import ajax_required
from .models import Visit


@ajax_required
def visit_view(request, ct, pk):
    """
    This view should be used along with some front-end scripts.
    This way we can exclude robots from records.
    """
    visit = Visit.objects.create(ip=get_ip(request), content_type_id=ct, object_id=pk)
    return HttpResponse(json.dumps({'id': visit.pk, }), content_type="application/json")
