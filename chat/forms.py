from django import forms

from .models import User

class ChatForm(forms.Form):
    username = forms.CharField(label='Username', max_length=200, required=True)
    room_name = forms.CharField(label='Room name', max_length=200, required=True)
    room_password = forms.CharField(label='Room password', max_length=200, required=False)
