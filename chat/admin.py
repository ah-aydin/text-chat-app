from django.contrib import admin

from .models import User, Message, Chat, HasAccess

@admin.register(User)
class AdminUser(admin.ModelAdmin):
    pass

@admin.register(Message)
class AdminMessage(admin.ModelAdmin):
    pass

@admin.register(Chat)
class AdminRoom(admin.ModelAdmin):
    pass

@admin.register(HasAccess)
class AdminHasAccess(admin.ModelAdmin):
    pass