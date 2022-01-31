Text Chat App
=============

A text chat application with temporary chat rooms and users where all data is discarded after the owner of the chat closes the conversation.

Environment setup
-----------------

Install redis:
```
sudo apt install redis
```

Create a python environment and run after activation:

```
pip install django djangorestframework redis django-redis channels channels-redis
```

Make migrations:
```
python manage.py makemigrations
python manage.py migrate
```

Run server:
```
python manage.py runserver
```