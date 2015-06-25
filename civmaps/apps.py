from django.apps import AppConfig

from django.utils.translation import ugettext_lazy as _


class CivMapsConfig(AppConfig):
    name = 'civmaps'
    verbose_name = _("Site Maps")
