from django.http import HttpResponseBadRequest, HttpResponseForbidden, JsonResponse, HttpResponse
from social.apps.django_app.utils import psa
from social.apps.django_app.default.models import UserSocialAuth

from oauth2_provider.settings import oauth2_settings
from oauthlib.common import generate_token
from oauth2_provider.models import AccessToken, Application
from django.utils.timezone import now, timedelta
from oauth2_provider.decorators import protected_resource
import traceback


def get_access_token(user):
    """
    Takes a user instance and return an access_token instance.
    """

    # our oauth2 app
    app = Application.objects.get(name="VaiTerCopaSim")

    # Deletes the old access_token
    try:
        AccessToken.objects.get(user=user, application=app).delete()
    except:
        pass

    # we generate an access token
    token = generate_token()

    expires = now() + timedelta(seconds=oauth2_settings.
                                ACCESS_TOKEN_EXPIRE_SECONDS)
    scope = "read write"

    # we create the access token
    access_token = AccessToken.objects. \
        create(user=user,
               application=app,
               expires=expires,
               token=token,
               scope=scope)

    response_token = {
        'access_token': access_token.token,
        'expires_in': oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS,
        'token_type': 'Bearer',
        'scope': access_token.scope
    }

    return response_token


@psa()
def auth_by_token(request, backend):
    user = request.backend.do_auth(request.REQUEST.get('access_token'))
    if user and user.is_active:
        return user
    return None


def social_register(request):
    try:
        user = auth_by_token(request, 'facebook')
        if user:
            return JsonResponse(get_access_token(user))
    except Exception as err:
        import traceback
        print traceback.format_exc()
        return HttpResponseBadRequest(str(err))

    return HttpResponseForbidden()


@protected_resource()
def revoke_token(request):
    # Deletes the access_token
    try:
        app = Application.objects.get(name="VaiTerCopaSim")
        user = request.resource_owner
        AccessToken.objects.get(user=user, application=app).delete()
    except:
        print 'User %s tried to revoke his token but an error happened. Please, see the stacktrace below' %(user.useremail)
        print traceback.format_exc()

    finally:
        return HttpResponse()
