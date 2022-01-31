from multiprocessing.sharedctypes import Value
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    """
    Manager for the custom user class below
    """
    def create_user(self, username, password=None):
        if not username: raise ValueError("A username must be provided")

        user = self.model(
            username=username
        )
        # No need for a password in this case
        user.save()
        return user
    
    def create_superuser(self, username):
        return self.create_user(username)

class User(AbstractBaseUser):
    """
    Temporary user
    """
    username            = models.CharField(max_length=200, unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['username',]

    object = UserManager

    # Required fields and methods by AbstractBaseUser
    is_active       = models.BooleanField(verbose_name='is active', default=False)
    is_staff        = models.BooleanField(verbose_name='is staff', default=False)
    is_admin        = models.BooleanField(verbose_name='is admin', default=False)

    # No permissions
    def has_perm(self, perm, obj=None):
        return False

    def has_module_perms(self, app_label):
        return False

    def __str__(self):
        return self.username

class Chat(models.Model):
    """
    Temporary chat
    """
    owner               = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    name                = models.CharField(max_length=200, null=False, unique=True, primary_key=True)
    participant_count   = models.IntegerField(default=1, null=False)
    password            = models.CharField(max_length=200, null=True, default=None)

    def __str__(self):
        return self.name

class Message(models.Model):
    room                = models.ForeignKey(Chat, on_delete=models.CASCADE)
    owner               = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    owner_name          = models.CharField(max_length=200, default='')
    content             = models.CharField(max_length=512)
    time_created        = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        try:
            username = self.owner.username
        except Exception:
            username = 'None'
        return f"{username} - {self.content[:50]}"
    
    class Meta:
        ordering = ('time_created',)

class HasAccess(models.Model):
    user                = models.OneToOneField(User, on_delete=models.CASCADE, related_name='access', unique=True)
    chat                = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='accesses')

    def __str__(self):
        return f"{self.user.username} - {self.chat.name}"