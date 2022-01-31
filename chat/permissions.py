from rest_framework import permissions

from .models import HasAccess

class HasAccessOrNone(permissions.BasePermission):
    """
    Allow read access only to those who have access to the chat
    """
    def has_permission(self, request, view):
        if str(request.user) == 'AnonymousUser':
            return False
        try:
            HasAccess.objects.get(user=request.user)
            return True
        except HasAccess.DoesNotExist:
            return False
