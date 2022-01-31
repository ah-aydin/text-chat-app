from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='chat-index'),
    path('connect/', views.connect, name='chat-connect'),
    path('create/', views.create, name='chat-create'),
    path('room/<str:room_name>/', views.room, name='chat-room')
]