from django.contrib import admin
from django.urls import path, include, reverse

from django.http.response import HttpResponseRedirect

# Simple redirect to the chat index page
def index(request):
    return HttpResponseRedirect(reverse('chat-index'))

urlpatterns = [
    path('admin/', admin.site.urls),

    # Application urls
    path('', index, name='index'),
    path('chat/', include('chat.urls')),
    # Rest API urls
    path('chat/api/', include('chat.urls_rest'))
]
