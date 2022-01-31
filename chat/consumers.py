import json
from channels.auth import logout
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Message, Chat, User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'room_{self.room_name}'
        self.room, self.room_owner_username = await self.get_room()

        if self.room:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            print(f"CONNECT '{str(self.scope['user'])}' TO '{self.room_name}'")

    async def disconnect(self, code):
        # Check if the user is the owner of the room
        username = str(self.scope['user'])
        room_removed = await self.check_room_ownership(username)

        # Logout user from session and delete account
        print(f"DISCONNECT '{username}' FROM '{self.room_name}'")
        await logout(self.scope)
        await self.remove_user(username)

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        # If the room has been deleted, notify the other consumers
        if room_removed:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'owner_left',
                }
            )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        time_created = text_data_json['time_created']

        # Create entry for the message in the database
        owner = await self.get_user(username)
        await self.create_message(owner, message, username)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'room_message',
                'message': message,
                'username': username,
                'time_created': time_created
            }
        )
    
    async def room_message(self, event):
        message = event['message']
        username = event['username']
        time_created = event['time_created']

        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': message,
            'username': username,
            'time_created': time_created
        }))
        
    async def owner_left(self, event):
        await self.send(text_data=json.dumps({
            'type': 'owner_left'
        }))

    @database_sync_to_async
    def get_room(self):
        try:
            room = Chat.objects.get(name=self.room_name)
            return room, room.owner.username
        except Chat.DoesNotExist:
            return None, ''
    
    @database_sync_to_async
    def get_user(self, username):
        return User.objects.get(username=username)
    
    @database_sync_to_async
    def remove_user(self, username):
        try:
            User.objects.get(username=username).delete()
        except Exception:
            pass

    @database_sync_to_async
    def create_message(self, owner, content, username):
        Message.objects.create(room=self.room, owner=owner, content=content, owner_name=username)
    
    @database_sync_to_async
    def check_room_ownership(self, username):
        # Remove room if owned by user
        try:
            if self.room_owner_username == username:
                self.room.delete()
                print(f"DELETE ROOM '{self.room_name}'")
                return True
            return False
        except:
            return False
