from django.http import JsonResponse
from models import *


# Create your views here.
def get_sticker(request, sticker_id=1):
    print sticker_id
    s = Sticker.objects.get(pk=sticker_id)
    return JsonResponse(s.dict())


def get_needed_stickers(request, user_id):
    needed = NeededStickers.objects.find(user__id=user_id)
    return JsonResponse(needed.dict())


def get_duplicated_stickers(request, user_id):
    duplicated = DuplicatedStickers.objects.find(user__id=user_id)
    return JsonResponse(duplicated.dict())


def get_statistics(request, user_id):
    return JsonResponse(NeededStickers.calculate_stats(user_id))


def add_needed_sticker(request, user_id, sticker_id):
    user = User.objects.get(pk=user_id)
    sticker = Sticker.objects.get(pk=sticker_id)
    n = NeededStickers(user=user, sticker=sticker)
    n.save()


def add_duplicated_sticker(request, user_id, sticker_id, quantity=1):
    user = User.objects.get(pk=user_id)
    sticker = Sticker.objects.get(pk=sticker_id)
    n = DuplicatedStickers(user=user, sticker=sticker, quantity=quantity)
    n.save()


def del_sticker(request, sticker_id):
    pass


def compare(request, user_id):
    pass


def search_user(request):
    pass

