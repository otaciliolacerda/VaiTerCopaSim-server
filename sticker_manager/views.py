from django.http import JsonResponse
from models import *


# Create your views here.
def get_sticker(request, sticker_id=1):
    print sticker_id
    s = Sticker.objects.get(pk=sticker_id)
    return JsonResponse(s.dict())


def add_sticker(request):
    pass


def del_sticker(request, sticker_id):
    pass


def get_stats(request, sticker_id):
    pass


def compare(request, user_id):
    pass


def search_user(request):
    pass

