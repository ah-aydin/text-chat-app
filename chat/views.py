from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .auth import login, logout
from .forms import ChatForm
from .models import User, Chat, HasAccess

def index(request):
    logout(request)
    return render(request, 'chat/index.html')

def connect(request):
    logout(request)

    form = ChatForm()

    # On form submit
    if request.method == 'POST':
        data = request.POST
        # See if chat with given name exists
        try:
            chat = Chat.objects.get(name=data['room_name'])
            # Check if there is password, if so check if it the correct one
            if chat.password != None:
                if chat.password != data['room_password']:
                    raise Exception('Wrong password')
        except Exception:
            return render(
                request, 
                'chat/connect.html', 
                {
                    'form': form, 
                    'error': 'Wrong room name and password combination' 
                }
            )
        
        # Create the user and give access to the chat
        try:
            user = User.objects.create(username=data['username'])
        except Exception:
            return render(request, 'chat/connect.html', { 'form': form, 'error': 'This username has been taken'})
        chat.participant_count += 1
        chat.save()
        HasAccess.objects.create(user=user, chat=chat)

        form = ChatForm(data)
        if form.is_valid():
            # Authenticate new user
            login(request, user)
            return HttpResponseRedirect(reverse('chat-room', kwargs={ 'room_name': data['room_name'] }))

    return render(request, 'chat/connect.html', { 'form': form })

def create(request):
    logout(request)

    form = ChatForm()

    # On form submit
    if request.method == 'POST':
        data = request.POST
        # Create the user and the chat objects
        try:
            user = User.objects.create(username=data['username'])
        except Exception :
            return render(request, 'chat/create.html', { 'form': form, 'error': 'This username has been taken.' })
        try:
            chat = Chat.objects.create(owner=user, name=data['room_name'], password=data['room_password'])
        except Exception:
            return render(request, 'chat/create.html', { 'form': form, 'error': 'This chat room name has been taken.'})
        # Give access for the owner in the chat
        HasAccess.objects.create(user=user, chat=chat)

        form = ChatForm(request.POST)
        if form.is_valid():
            # Authenticate new user and redirect to chat room
            login(request, user)
            return HttpResponseRedirect(reverse('chat-room', kwargs={ 'room_name': data['room_name']}))

    return render(request, 'chat/create.html', { 'form': form })

def room(request, room_name):
    if request.user.is_anonymous: return HttpResponseRedirect(reverse('chat-index'))
    username = request.user.username
    # Check if there is a user, there is a room with the given name and that
    # the user has access to this room
    try:                            
        user = User.objects.get(username=username)
        chat_room = Chat.objects.get(name=room_name)
        HasAccess.objects.get(user=user, chat=chat_room)
    except Exception:
        return HttpResponseRedirect(reverse('chat-index'))

    # Show room
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'username': username
    })