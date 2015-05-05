from __future__ import unicode_literals
import datetime

from django.core.management.base import NoArgsCommand
from django.db.models import Q, F, Count

from postman.models import Message


class Command(NoArgsCommand):
    help = "Can be run as a cron job or directly to check-up data consistency in the database."

    def handle_noargs(self, **options):
        verbose = int(options.get('verbosity'))
        if verbose >= 1:
            self.stdout.write(datetime.datetime.now().strftime("%H:%M:%S ") + "Checking messages and conversations for inconsistencies...\n")
        checks = [
            ("Sender and Recipient cannot be both undefined.", Q(sender__isnull=True, recipient__isnull=True)),
            ("Visitor's email is in excess.", Q(sender__isnull=False, recipient__isnull=False) & ~Q(email='')),
            ("Visitor's email is missing.", (Q(sender__isnull=True) | Q(recipient__isnull=True)) & Q(email='')),
            ("Reading date must be later to sending date.", Q(read_at__lt=F('sent_at'))),
            ("Deletion date by sender must be later to sending date.", Q(sender_deleted_at__lt=F('sent_at'))),
            ("Deletion date by recipient must be later to sending date.", Q(recipient_deleted_at__lt=F('sent_at'))),
            ("Response date must be later to sending date.", Q(replied_at__lt=F('sent_at'))),
            ("The message cannot be replied without having been read.", Q(replied_at__isnull=False, read_at__isnull=True)),
            ("Response date must be later to reading date.", Q(replied_at__lt=F('read_at'))),
            # because of the delay due to the moderation, no constraint between replied_at and recipient_deleted_at
            ("Response date cannot be set without at least one reply.",
                Q(replied_at__isnull=False), {'cnt': Count('next_messages')}, Q(cnt=0)),
                # cnt should filter to allow only accepted replies, but do not know how to specify it
            ("The message cannot be replied without being in a conversation.",
                Q(replied_at__isnull=False, thread__isnull=True)),
            ("The message cannot be a reply without being in a conversation.",
                Q(parent__isnull=False, thread__isnull=True)),
            ("The reply and its parent are not in a conversation in common.",
                Q(parent__isnull=False, thread__isnull=False) & (Q(parent__thread__isnull=True) | ~Q(parent__thread=F('thread')))),
        ]
        count = 0
        for c in checks:
            msgs = Message.objects.filter(c[1])
            if len(c) >= 4:
                msgs = msgs.annotate(**c[2]).filter(c[3])
            if msgs:
                count += len(msgs)
                self.report_errors(c[0], msgs)
        if verbose >= 1:
            self.stdout.write(datetime.datetime.now().strftime("%H:%M:%S ") +
                ("Number of inconsistencies found: {0}. See details on the error stream.\n".format(count) if count
                else "All is correct.\n"))

    def report_errors(self, reason, msgs):
        self.stderr.write(reason + '\n')
        self.stderr.write("  {0:6} {1:5} {2:5} {3:10} {4:6} {5:6} {6:16} {7:16} {8:16}\n".format(
            "Id","From","To","Email","Parent","Thread","Sent","Read","Replied"))
        for msg in msgs:
            self.stderr.write(
                "  {0.pk:6} {0.sender_id:5} {0.recipient_id:5} {0.email:10.10} {0.parent_id:6} {0.thread_id:6}"
                " {0.sent_at!s:16.16} {0.read_at!s:16.16} {0.replied_at!s:16.16}\n".format(msg))
