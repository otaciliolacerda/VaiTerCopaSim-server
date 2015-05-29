__author__ = 'otacilio'

from django.conf.urls import url
from auth.views import *


urlpatterns = [
    url(r'^login/$', social_register, name='social_register'),
    url(r'^logout/$', revoke_token, name='revoke_token'),
]
