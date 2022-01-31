from django.urls import path

from . import views_rest as views

urlpatterns = [
    path('messages/<str:room_name>/', views.MessageList.as_view(), name='chat-api-message-list'),
]