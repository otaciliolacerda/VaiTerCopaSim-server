__author__ = 'otacilio'

from django.conf.urls import url
from stickerAPI.views import *


urlpatterns = [
    url(r'^sticker/(?P<user_id>[0-9]+)/needed/$', needed_stickers, name='needed_stickers'),
    ]