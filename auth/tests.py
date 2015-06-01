from django.test import TestCase
import views
from stickerAPI.tests import RequestTestHelper
from stickerAPI.seed import seed
from mock import Mock
from oauth2_provider.models import AccessToken, Application


class AuthorizationTests(TestCase):

    def setUp(self):
        # Set up data for the whole TestCase
        users = seed(True)
        self.user, self.token = users[0].get('user'), users[0].get('token')
        self.user.social_user = Mock(uid=1)
        self.helper = RequestTestHelper('/api/v1/auth/login/', self.token)

    def test_login_new_user(self):
        data = {'access_token': 'valid_facebook_token'}

        #mock the facebook token validation
        views.auth_by_token = Mock(return_value=self.user)

        request = self.helper.get_request('get', data)
        response = views.social_register(request)

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)

    def test_login_invalid_user(self):
        data = {'access_token': 'invalid_facebook_token'}

        #mock the facebook token validation
        views.auth_by_token = Mock(return_value=None)

        request = self.helper.get_request('get', data)
        response = views.social_register(request)

        self.assertEqual(response.status_code, 403)

    def test_api_call_using_invalid_user(self):
        data = {'token': '1'}

        request = self.helper.get_request('delete', data)

        #this makes the user invalid (invalid token)
        request.META['HTTP_AUTHORIZATION'] = 'Bearer INVALID_TOKEN'
        response = views.revoke_token(request)

        self.assertEqual(response.status_code, 403)

    def test_revoke_token(self):
        data = {'access_token': 'valid_facebook_token'}

        request = self.helper.get_request('get')
        response = views.revoke_token(request)

        self.assertEqual(response.status_code, 200)

        app = Application.objects.get(name="VaiTerCopaSim")
        self.assertFalse(AccessToken.objects.filter(user__id=self.user.id, application__id=app.id).exists())

    def test_get_access_token(self):
        token = views.get_access_token(self.user)

        self.assertEqual(len(token.get('access_token')), 30)
        self.assertEqual(token.get('token_type'), 'Bearer')
        self.assertEqual(token.get('scope'), 'read write')
        self.assertEqual(token.get('expires_in'), 36000)