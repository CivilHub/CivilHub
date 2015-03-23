# -*- coding: utf-8 -*-
import os, time, hashlib, random, string

from slugify import slugify
from itertools import chain
from uuid import uuid4 as uuid
from datetime import datetime
from PIL import Image

from django.core.files import File
from django.conf import settings
from django.utils import translation
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from actstream.models import Action, user_stream

from .models import UserProfile


AVATAR_IMG_PATH = os.path.join(settings.MEDIA_ROOT, 'img/avatars')


def create_user_profile(user, **kwargs):
    """
    Metoda przyjmuje jako argument instancję auth.user i tworzy profil użytkownika.
    """
    try:
        profile = UserProfile(user=user)
    except Exception:
        return None
    language = kwargs.get('language', settings.LANGUAGE_CODE)
    if translation.check_for_language(language):
        profile.lang = language
    profile.save()
    return profile


def profile_activation(user, **kwargs):
    """ Sprawdzamy, czy profil użytkownika istnieje lub tworzymy nowy. """
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = create_user_profile(user, **kwargs)
    if profile is None:
        raise Exception(u"Cannot create or fetch user profile")
    return profile


def random_string(length=8):
    """ Funkcja tworzy ciąg losowych znaków alfanumerycznych. """
    return ''.join(random.choice(string.letters + string.digits) for _ in range(length))


def random_username():
    """ Funkcja tworząca losową i unikalną nazwę użytkownika. """
    username = random_string(30)
    while (User.objects.filter(username=username).count() > 0):
        username = random_string(30)
    return username


def create_username(first_name, last_name):
    """
    Próbujemy utworzyć "czystą" nazwę użytkownika na podstawie imienia i nazwiska.
    """
    if first_name is None or not len(first_name):
        first_name = None
    if last_name is None or not len(last_name):
        last_name = None

    if first_name is None and last_name is None:
        return random_username()
    elif first_name is None:
        raw_username = slugify(last_name)
    elif last_name is None:
        raw_username = slugify(first_name)
    else:
        raw_username = "{}_{}".format(slugify(first_name), slugify(last_name))

    retries = 0
    username = raw_username
    while User.objects.filter(username=username).count():
        retries += 1
        username = "{}_{}".format(raw_username, retries)
    return username


def random_password():
    """
    Funkcja tworzy losowy ciąg znaków zakodowany w MD5 (32 znaki).
    """
    salt = hashlib.md5()
    salt.update(settings.SECRET_KEY + str(datetime.now().time))
    return salt.hexdigest()


def delete_thumbnails(imgfile):
    """
    Delete all thumbnails related to user avatar image. This function takes
    image filename as argument and looking for all thumbnails which names
    contains this filename.
    """
    imgfile = os.path.splitext(imgfile)[0]
    for f in os.listdir(AVATAR_IMG_PATH):
        if imgfile in f: os.unlink(os.path.join(AVATAR_IMG_PATH, f))


def create_thumbnail(imgfile, size):
    """
    This function takes existing image file as argument and creates
    thumbnail according to given size, which must be tuple or list containing
    width and 
    """
    pathname = os.path.join(settings.MEDIA_ROOT, 'img/avatars/')
    img = Image.open(os.path.join(pathname, imgfile))
    file, ext = os.path.splitext(imgfile)
    thumbname = str(size[0])+'x'+str(size[1]) + '_' + file + ext
    img.thumbnail(size)
    img.save(os.path.join(pathname, thumbname), 'PNG')


def avatar_thumbnails(filename):
    """
    This function takes existing image file as argument and create apropriate
    thumbnails according to AVATAR_THUMBNAIL_SIZES setting.
    """
    for s in settings.AVATAR_THUMBNAIL_SIZES:
        create_thumbnail(filename, s)


def crop_avatar(imgfile):
    """
    Crop image avatr picture to make it fit into rectangular area. Returns
    Django File object.
    
    You can pass either python file instance or PIL image instance to this
    function.
    """
    if str(type(imgfile)) == "<type 'instance'>":
        img = imgfile
    else:
        img = Image.open(imgfile)
    pathname = 'img/avatars'
    dirname = os.path.join(settings.MEDIA_ROOT, pathname)
    imgname = str(uuid()) + str(len(os.listdir(dirname))) + '.png'
    imgpath = os.path.join(dirname, imgname)
    width, height = img.size
    s = width if width < height else height
    img = img.crop(((width - s) / 4, 0, s, s))
    if s > settings.AVATAR_SIZE[0]:
        img.thumbnail(settings.AVATAR_SIZE)
    img.save(imgpath, 'PNG')
    avatar_thumbnails(imgname)
    return File(open(imgpath))


def update_profile_picture(profile, image):
    """
    This function takes user profile instance along with image file and
    sets up proper avatars.
    """
    if not profile.has_default_avatar:
        try:
            os.unlink(profile.avatar.path)
            delete_thumbnails(profile.avatar.name.split('/')[-1:][0])
        except Exception:
            pass
    profile.avatar = crop_avatar(image)
    size = 60, 60
    path = os.path.join(settings.MEDIA_ROOT, 'img/avatars')
    file, ext = os.path.splitext(profile.avatar.name.split('/')[-1:][0])
    thumbname = '60x60_' + file + ext
    tmp = image.copy()
    tmp.thumbnail(size, Image.ANTIALIAS)
    tmp.save(os.path.join(path, thumbname))
    profile.thumbnail = 'img/avatars/' + thumbname
    profile.save()


class UserActionStream(object):
    """
    Generic object for custom user stream. I've tried to use actstream's
    method to achieve similar effects, but it turned to be too problematic.
    
    This class manages user's actions, not his action streams (despite it's
    name). It is included to show and count actions performed by user, related
    to user and his/her profile.
    """
    def __init__(self, user):
        """
        Initialize actstream.
        @param user django.contrib.auth.models.User instance
        """

        # Django's contrib User instance
        self.user = user
        # User object content type
        self.content_type = ContentType.objects.get_for_model(self.user)
        # User object ID
        self.object_id    = self.user.pk
        # User profile content type
        self.profile_type = ContentType.objects.get_for_model(self.user.profile)
        # User profile ID
        self.profile_id   = self.user.profile.pk
        # Custom activity queryset
        self.stream       = self._get_queryset()


    def _get_queryset(self):
        """
        Get custom Action object queryset to replace built-in Activity Stream
        mechanism of fetching object-related actions.
        """
        # Actions for user
        actor    = Action.objects.filter(actor_content_type=self.content_type)
        actor    = actor.filter(actor_object_id=self.object_id)
        obj      = Action.objects.filter(action_object_content_type=self.content_type)
        obj      = obj.filter(action_object_object_id=self.object_id)
        target   = Action.objects.filter(target_content_type=self.content_type)
        target   = target.filter(target_object_id=self.object_id)
        # Actions for user profile
        p_actor  = Action.objects.filter(actor_content_type=self.profile_type)
        p_actor  = p_actor.filter(actor_object_id=self.profile_id)
        p_obj    = Action.objects.filter(action_object_content_type=self.profile_type)
        p_obj    = p_obj.filter(action_object_object_id=self.profile_id)
        p_target = Action.objects.filter(target_content_type=self.profile_type)
        p_target = p_target.filter(target_object_id=self.profile_id)

        self.actor_related  = actor  | p_actor
        self.obj_related    = obj    | p_obj
        self.target_related = target | p_target

        return actor | obj | target | p_actor | p_obj | p_target


    def get_actions_by_type(self, stream, content_type=None):
        """
        Get only actions related to given content type - e.g. only Ideas.
        
        Previously filtered stream must be provided as mandatory argument.
        This is where we start further filtering.
        
        If 'content_type' is provided in form of 'app_name.model_name' string,
        return only actions related to search item. Otherwise function returns
        all user actions.
        """
        if not content_type:
            return stream

        app_name, model_name = content_type.split('.')
        content_type = ContentType.objects.get_by_natural_key(app_name,
                                                              model_name)

        actor_actions  = stream.filter(actor_content_type=content_type)
        target_actions = stream.filter(target_content_type=content_type)
        object_actions = stream.filter(action_object_content_type=content_type)

        return actor_actions | target_actions | object_actions


    def get_actions(self, content_type=None, action_type=None):
        """
        Return django queryset containing list of all actions related
        to user and his/her profile.
        
        If 'content_type' is provided, actions will be filtered to only this
        related to given content type (in form of "app_name.model_name"
        string.
        
        If 'action_type' is provided, actions will be filtered that results
        will only contain actions where user acted as provided actstream
        element (e.g. 'actor', 'object' or 'target').
        """
        stream = self.stream

        if action_type == 'actor':
            stream = self.actor_actions()
        if action_type == 'object':
            stream = self.object_actions()
        if action_type == 'target':
            stream = self.target_actions()

        return self.get_actions_by_type(stream, content_type)


    def actor_actions(self):
        """
        Returns all actions where user or profile is actor.
        """
        return self.actor_related


    def object_actions(self):
        """
        Returns all actions where user or profile acts as action object.
        This is highly unlikely but not impossible.
        """
        return self.object_related


    def target_actions(self):
        """
        Returns all actions where user or profile is target.
        """
        return self.target_related
