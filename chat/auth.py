from urllib import request
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import login as li
from django.contrib.auth import logout as lo

from rest_framework import authentication
from rest_framework import exceptions

from .models import User

def login(request, user):
    """
    Helper method to authenticate with the custom backend
    """
    backend = 'chat.auth.ChatUserBackend'
    li(request, user, backend)

def logout(request):
    """
    Logout the current session user and remove it from the database
    """
    username = request.user.username
    lo(request)
    try:
        User.objects.get(username=username).delete()
    except User.DoesNotExist:
        pass

class ChatUserBackend(BaseBackend):
    """
    Authentication backend for the chat users
    """
    def authenticate(self, request, username=None):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

class ChatUserRESTAuthentication(authentication.BaseAuthentication):
    """
    Authentication class for REST api.
    Allow access only to the users who have logged in and have access to the room
    """
    def authenticate(self, request):
        username = request.META.get('HTTP_X_USERNAME')
        if not username:
            return None
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')
        
        return (user, None)