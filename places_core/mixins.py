# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.db.transaction import non_atomic_requests


class LoginRequiredMixin(object):
    """
    Mixin to allow only logged in users do certain actions
    """
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class AtomicFreeTransactionMixin(object):
    """
    Mixin to disable atomic transactions to avoid problems with
    "This is forbidden when 'atomic' block is enabled" error.
    """
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(AtomicFreeTransactionMixin, cls).as_view(**initkwargs)
        return non_atomic_requests(view)
