# -*- coding: utf-8 -*-
from actstream.managers import ActionManager, stream


class CivilActionManager(ActionManager):

    @stream
    def mystream(self, obj):
        return super(CivilActionManager, self).user(obj)
