from django.test import TestCase
from rest_framework.test import APISimpleTestCase

class TestChatApplicationViews(TestCase):
    
    def setUp(self):
        pass

    def test_create_chat(self):
        """
        Test chat create view.
        Anyone should be able to create a chat.
        """

    def test_chat_connect(self):
        """
        Test chat connect view.
        Should return to index page if it is anonymous user or wrong password.
        """

    def test_chat_delition(self):
        """
        Test if the chat gets deleted if there are no users left using it.
        """
    
    def test_chat_room(self):
        """
        test chat room view.
        Should return if no authenticated user found or user has no access to the chat room
        """

class TestChatAPI(APISimpleTestCase):
    
    def setUp(self):
        pass

    def test_get_messages(self):
        """
        Test if only the only people who can get messages from a chat are those which
        are part of it.
        """