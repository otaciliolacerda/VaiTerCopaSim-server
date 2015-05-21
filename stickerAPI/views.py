from django.http import JsonResponse
from models import *
from django.core.exceptions import ObjectDoesNotExist
from seed import *


# Create your views here.
def needed_stickers(request, user_id):
    #seed()
    stickers = request.REQUEST.get('stickers', None)
    print 'STICKERS_POST: ' + str(stickers)
    if stickers:
        sticker_list = stickers.split(',')
        for i in sticker_list:
            stick = None
            try:
                user = User.objects.get(pk=user_id)
                stick = Sticker.objects.get(number=i)
                NeededStickers.objects.get(sticker__number=i, user__id=user_id)
                return JsonResponse({})
            except ObjectDoesNotExist:
                NeededStickers(user=user, sticker=stick).save()
                return JsonResponse({})
    else:
        needed = NeededStickers.objects.filter(user__id=user_id)
        print "NEEDED: " + str(needed)
        return JsonResponse([i.dict() for i in needed], safe=False)