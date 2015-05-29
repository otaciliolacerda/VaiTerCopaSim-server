from django.test import TestCase
from django.test import Client
from views import *
from django.http import JsonResponse


class AuthorizationTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        #seed()
        pass

    def test_register_new_user(self):
        client = Client()
        response = client.get('/auth/social/')

        self.assertEqual(response.status_code, 200)

