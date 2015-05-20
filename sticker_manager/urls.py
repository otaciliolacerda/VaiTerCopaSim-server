__author__ = 'otacilio'

from django.conf.urls import include, url
from sticker_manager.views import *


urlpatterns = [
    url(r'^$', get_sticker),
    url(r'^(?P<sticker_id>[0-9]+)/$', get_sticker, name='show'),
    url(r'^(?P<user_id>[0-9]+)/$', get_needed_stickers, name='get_needed_stickers'),
    url(r'^(?P<user_id>[0-9]+)/$', get_duplicated_stickers, name='get_duplicated_stickers'),
    url(r'^(?P<user_id>[0-9]+)/$', get_statistics, name='get_statistics'),
    ]