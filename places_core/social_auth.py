# -*- coding: utf-8 -*-
import os
import json
import urllib
import urllib2

from PIL import Image

from django.conf import settings
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from social.apps.django_app.default.models import UserSocialAuth
from social.pipeline.partial import partial
from social.exceptions import AuthException
from rest_framework.authtoken.models import Token

from civmail.messages import FriendsEmail, NewFriendEmail
from userspace.models import UserProfile
from userspace.helpers import random_string, create_username, update_profile_picture


def notify_friends(user, fb_id_list):
    if not len(fb_id_list):
        return
    friends = []
    for sa in UserSocialAuth.objects.filter(provider='facebook'):
        if int(sa.extra_data.get('id')) in fb_id_list:
            friends.append(sa.user.pk)
    users = User.objects.filter(pk__in=friends)
    domain = Site.objects.get_current().domain
    if len(friends):
        FriendsEmail().send(user.email, {
            'baseurl': domain,
            'lang': user.profile.lang,
            'friends': users, })
    for friend in users:
        NewFriendEmail().send(friend.email, {
            'baseurl': domain,
            'lang': friend.profile.lang,
            'inviting_user': user, })


def obtain_user_social_profile(response):
    """ Get user social profile url. """
    if 'link' in response:
        return response['link']
    elif 'url' in response:
        return response['url']
    return u''


def obtain_user_gender(response):
    """ Get user's gender and convert to proper format. """
    if not 'gender' in response:
        return None
    elif response['gender'] == 'female':
        return 'F'
    elif response['gender'] == 'male':
        return 'M'
    return 'U'


def set_user_profile_birth_date(date_string):
    """ Try to get user's birth date and convert to python date format. """
    try:
        return date_string.split(' ')[0]
    except Exception:
        return None


def validate_email(strategy, details, user=None, social=None, *args, **kwargs):
    """
    We binding user accounts via email. If user with this email already exists,
    the new association will be bind to this user automatically. THIS IS WRONG!
    """
    email = details.get('email', '')
    if not email or email == '':
        strategy.session_set('auth_error', True)
        return strategy.redirect(reverse('user:s_auth_error'))
    try:
        system_user = User.objects.get(email=details.get('email'))
    except User.DoesNotExist:
        system_user = None
        strategy.session_set('new_user', True)
    if user is None and system_user != None:
        return {'social': social,
                'user': system_user,
                'new_association': True}


@partial
def set_twitter_email(strategy, details, user=None, is_new=False, *args, **kwargs):
    """ Get email address from users authorized via Twitter account. """
    if kwargs['backend'].name == 'twitter' and is_new:
        email = strategy.session_pop('account_email')
        if email:
            details['email'] = email
        else:
            return strategy.redirect(reverse('user:twitter_email'))


def update_user_social_profile(strategy, details, response, user, *args, **kwargs):
    """ Try to get additional social links for this user. """
    changed = False
    profile = UserProfile.objects.get(user=user)
    if kwargs['backend'].name == 'facebook' and not profile.fb_url:
        profile.fb_url = obtain_user_social_profile(response)
        changed = True
    elif kwargs['backend'].name == 'google-plus' and not profile.gplus_url:
        profile.gplus_url = obtain_user_social_profile(response)
        changed = True
    if 'gender' in response and not profile.gender:
        profile.gender = obtain_user_gender(response)
        changed = True
    if 'birthday' in response and not profile.birth_date:
        profile.birth_date = set_user_profile_birth_date(response['birthday'])
        changed = True
    if kwargs['backend'].name == 'twitter' and not profile.twt_url:
        try:
            screen_name = response['access_token']['screen_name']
            profile.twt_url = 'https://twitter.com/' + screen_name
            changed = True
        except KeyError, TypeError:
            pass
    if kwargs['backend'].name == 'linkedin' and not profile.linkedin_url:
        try:
            profile.linkedin_url = response['publicProfileUrl']
            changed = True
        except KeyError:
            pass
    if changed: profile.save()


def create_user_profile(strategy, details, response, user=None, *args, **kwargs):
    """
    Create token for user to be used in REST application. It allows users to
    login with mobile application.
    """
    if user:
        token = Token.objects.get_or_create(user=user)


def get_username(strategy, details, user=None, *args, **kwargs):
    """ Create username. Try to join first an last name if possible. """
    storage = strategy.storage
    if user:
        final_username = storage.user.get_username(user)
    else:
        final_username = create_username(details.get('first_name'),
                                         details.get('last_name'))
    return {'username': final_username}


def get_friends(strategy, details, response, user, *args, **kwargs):
    """ Get list of Facebook user's friends that already are registered in
        our application.
    """
    # This function is appropriate only for Facebook accounts
    if kwargs['backend'].name != 'facebook':
        return

    # There is no point for sending email any time user log in
    if not kwargs['is_new']:
        return

    url = 'https://graph.facebook.com/{}/friends?{}'
    params = urllib.urlencode({
        'access_token': response['access_token'],
        'fields': ['id', ], })

    res = json.loads(urllib2.urlopen(url.format(response['id'], params)).read())

    notify_friends(user, [int(x['id']) for x in res['data']])


def get_user_avatar(strategy, details, response, user, *args, **kwargs):
    """ Try to get user profile avatar from social networks.
    """
    image_url = None
    is_default = True
    TMP_FILE = os.path.join(settings.BASE_DIR, 'media/tmp/image')

    # Get image info from social sites
    if kwargs['backend'].name == 'twitter':
        image_url = response.get('profile_image_url_https').replace('_normal', '')
        is_default = response.get('default_profile_image')

    elif kwargs['backend'].name == 'facebook':
        base_url = 'https://graph.facebook.com/{}/picture?{}'
        data = json.loads(urllib.urlopen(base_url.format(response.get('id'),
                                                    'redirect=false')).read())
        if not data.get('is_silhouette'):
            image_url = base_url.format(response.get('id'), 'type=large')
            is_default = False

    elif kwargs['backend'].name == 'google-plus':
        is_default = response.get('image')['isDefault']
        if not is_default:
            image_url = response.get('image')['url'].replace('sz=50', 'sz=200')

    # Download image and replace profile avatar
    if image_url is not None and not is_default and user.profile.has_default_avatar:
        urllib.urlretrieve(image_url, TMP_FILE)
        image = Image.open(TMP_FILE)
        try:
            update_profile_picture(user.profile, image)
        except Exception:
            pass
