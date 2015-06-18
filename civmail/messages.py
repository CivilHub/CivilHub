# -*- coding: utf-8 -*-
from djmail import template_mail


class TestTemplateEmail(template_mail.TemplateMail):
    """
    This is test class. It's only purpose is to test sending email in Django
    mail system. This email class uses templates to construct message body
    and header. Templates could be found in 'templates/emails' directory.
    Template names are always related to below 'name' class parameter.
    """
    name = "test_mail"


class FollowersNotificationMesage(template_mail.TemplateMail):
    """ Send this message to all followers of chosen location as
    well as to followers of it's children locations. """
    name = "followers"


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


class ServicePollMail(template_mail.TemplateMail):
    """
    Send this email after some time to every registered user to get feedback
    about service functionality.
    """
    name = "service"


class UserStreamMail(template_mail.TemplateMail):
    """
    Send this message once a week to users which wants to be informed about
    activities in places they follow. In practice this is part of user stream.
    """
    name = "activities"


class InviteToOrganization(template_mail.TemplateMail):
    """
    Send this email when organization creator wants to invite users to his/her
    organization.
    """
    name = "organization"


class PostmanNotifyMail(template_mail.TemplateMail):
    """ Custom message for Postman notification.
    """
    name = "postman"


class MassMailTemplate(template_mail.TemplateMail):
    """ Simple newsletter functionality.
    """
    name = "newsletter"


class ContactEmail(template_mail.TemplateMail):
    """ Email sent when user filled contact form.
    """
    name = "contact_mail"


class ContactResponseEmail(template_mail.TemplateMail):
    """ Email to send in response for contact message.
    """
    name = "response_mail"


class LastLoginNotifyEmail(template_mail.TemplateMail):
    """ Email with invitation to login again for users that
        were not active during selected time period.
    """
    name = "remind"


class FriendsEmail(template_mail.TemplateMail):
    """ Send this email to new Facebook user with notification about his FB
        friends already registered in system.
    """
    name = "friends"


class NewFriendEmail(template_mail.TemplateMail):
    """ Send this message to all Facebook friends of newly logged in user and
        inform them that they frind joined Civilhub.
    """
    name = "new_friend"


class IdeaStatusEmail(template_mail.TemplateMail):
    """ Sent to idea's author when it's status changes.
    """
    name = "idea_status"
