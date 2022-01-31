from rest_framework import generics

from .models import Message
from .permissions import HasAccessOrNone
from .serializers import MessageSerializer

class MessageList(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [HasAccessOrNone]
    def get_queryset(self):
        room_name = self.kwargs['room_name']
        return Message.objects.filter(room__name=room_name)
    