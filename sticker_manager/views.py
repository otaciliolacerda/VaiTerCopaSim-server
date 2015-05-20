from django.http import JsonResponse
from models import *


# Create your views here.
def get_sticker(request, sticker_id=1):
    print sticker_id
    s = Sticker.objects.get(pk=sticker_id)
    return JsonResponse({'number': s.number, 'order': s.order, 'name': s.name, 'team': s.team, 'image': s.image})


def add_sticker(request):
    pass


def del_sticker(request):
    pass


def get_stats(request):
    pass


def compare(request):
    pass


def search_user(request):
    pass

