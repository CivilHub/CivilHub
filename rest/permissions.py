from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Write permissions are only allowed to the owner of the snippet.
        if hasattr(obj, 'user'):
            return obj.user == request.user

        return False


class IsModeratorOrReadOnly(permissions.BasePermission):
    """
    Custom permission for moderators allowing them to create
    and manipulate object instances within locations that they
    manage.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Always allowed for superadmins
        if request.user.is_superuser:
            return True

        # allow only for moderators
        try:
            return obj.location in request.user.locations.all()
        except AttributeError:
            return False
