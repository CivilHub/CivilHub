Places
======

Note
----
Because of obsolete url config usage I have changed first line in urls.py for
django-activity-stream from

    from django.conf.urls.defaults import *
    
to
    
    rom django.conf.urls import *
    
Also changed django-activity-stream 'action.html' template as explained here:

    https://github.com/justquick/django-activity-stream/commit/c11b226d12f229170d3348fd5174769f1e704989
    
Changed extend tag in django-activity-stream templates to point to our base.html

Paczka z templatami do django-activity: https://bitbucket.org/krastley/places/downloads/templates.tar.bz2
urls.py: https://bitbucket.org/krastley/places/downloads/urls.py