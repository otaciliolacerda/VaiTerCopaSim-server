from django.test import TestCase
from views import *
from stickerAPI.tests import RequestTestHelper
from stickerAPI.seed import seed


class AuthorizationTests(TestCase):

    def setUp(self):
        # Set up data for the whole TestCase
        self.user, self.token = seed(True)
        self.helper = RequestTestHelper('/api/v1/auth/login/', self.token)

    def test_register_new_user(self):
        pass

    def test_should_return_401_if_user_is_invalid(self):
        data = {'token': '1'}

        request = self.helper.get_request('delete', data)

        #this makes the user invalid (invalid token)
        request.META['HTTP_AUTHORIZATION'] = 'Bearer INVALID_TOKEN'
        response = revoke_token(request)

        self.assertEqual(response.status_code, 403)

