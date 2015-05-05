from __future__ import unicode_literals
from datetime import timedelta
from optparse import make_option

from django.core.management.base import NoArgsCommand
from django.db.models import Max, Count, F, Q
try:
    from django.utils.timezone import now   # Django 1.4 aware datetimes
except ImportError:
    from datetime import datetime
    now = datetime.now

from postman.models import Message


class Command(NoArgsCommand):
    help = """Can be run as a cron job or directly to clean out old data from the database:
  Messages or conversations marked as deleted by both sender and recipient,
  more than a minimal number of days ago."""
    option_list = NoArgsCommand.option_list + (
        make_option('-d', '--days', type='int', default=30,
            help='The minimal number of days a message is kept marked as deleted, '
                 'before to be considered for real deletion [default: %default]'),
        )

    def handle_noargs(self, **options):
        verbose = int(options.get('verbosity'))
        days = options.get('days')
        date = now() - timedelta(days=days)
        if verbose >= 1:
            self.stdout.write("Erase messages and conversations marked as deleted before %s\n" % date)
        # for a conversation to be candidate, all messages must satisfy the criteria
        tpks = Message.objects.filter(thread__isnull=False).values('thread').annotate(
                cnt=Count('pk'),
                s_max=Max('sender_deleted_at'),    s_cnt=Count('sender_deleted_at'),
                r_max=Max('recipient_deleted_at'), r_cnt=Count('recipient_deleted_at')
            ).order_by().filter(
                s_cnt=F('cnt'), r_cnt=F('cnt'), s_max__lte=date, r_max__lte=date
            ).values_list('thread', flat=True)
        Message.objects.filter(
            Q(thread__in=tpks) |
            Q(thread__isnull=True, sender_deleted_at__lte=date, recipient_deleted_at__lte=date)
        ).delete()
