# -*- coding: utf-8 -*-
from djmail import template_mail

# Define a subclass of TemplateMail
class TestTemplateEmail(template_mail.TemplateMail):
    """
    This is test class. It's only purpose is to test sending email in Django
    mail system. This email class uses templates to construct message body
    and header. Templates could be found in 'templates/emails' directory.
    Template names are always related to below 'name' class parameter.
    """
    name = "test_mail"


class ActivationLink(template_mail.TemplateMail):
    """
    Send this email to every new registered user. It should include link
    generated during registration process.
    """
    name = "welcome"


class PasswordResetMail(template_mail.TemplateMail):
    """
    Send message containing new random password to user who wants reset pass.
    """
    name = "password"


class InviteUsersMail(template_mail.TemplateMail):
    """
    Send invitations to follow location to selected user/users.
    """
    name = "invite"


class InviteToContentMail(template_mail.TemplateMail):
    """
    Invite people to browse currently selected content by sending them email
    with hard link to this content.
    """
    name = "content"
