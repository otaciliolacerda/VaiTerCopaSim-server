__author__ = 'otacilio'

from django.conf.urls import url
from stickerAPI.views import *


urlpatterns = [
    url(r'^sticker/needed/$', needed_stickers, name='needed_stickers'),
    url(r'^sticker/duplicated/$', duplicated_stickers, name='duplicated_stickers'),
    url(r'^sticker/statistics/$', statistics, name='statistics'),
    ]