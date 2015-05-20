__author__ = 'otacilio'

from django.conf.urls import include, url
from sticker_manager.views import get_sticker


urlpatterns = [
    url(r'^$', get_sticker),
    url(r'^(?P<sticker_id>[0-9]+)/$', get_sticker, name='show'),
    ]