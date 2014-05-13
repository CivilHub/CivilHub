# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required


class LoginRequiredMixin(object):
    """
    Mixin to allow only logged in users do certain actions
    """
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)
