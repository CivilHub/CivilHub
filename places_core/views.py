from django.views.generic.edit import CreateView
from .models import AbuseReport


class CreateAbuseReport(CreateView):
    """
    Static form to create abuse reports for different ContentTypes.
    """
    model = AbuseReport
    template_name = 'places_core/abuse-report.html'

    def pre_save(self, obj):
        obj.sender = self.request.user
