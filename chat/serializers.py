from rest_framework import serializers, fields

from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    room_name = serializers.CharField(source='room.name')
    class Meta:
        model = Message
        fields = ('id', 'room_name', 'owner_name', 'content', 'time_created')