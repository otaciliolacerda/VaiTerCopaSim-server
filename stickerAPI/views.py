from django.http import *
from models import *
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from seed import *
import logging
import sys


log = logging.getLogger("[VaiTerCopaSim]")
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)


def logger(fn):
    '''
    Decorator function to log all view operations
    '''
    def inner(*args, **kwargs):
        name = str(fn.__name__)
        method = args[0].method
        log.debug('%s received an HTTP %s' % (name, method))

        response = fn(*args, **kwargs)

        response_class = response.__class__.__name__
        status_code = response.status_code
        log.debug('%s sent an HTTP Response of type %s with status code %s' % (name, response_class, status_code))
        return response
    return inner


def run_secure(operation, **kwargs):
    try:
        return operation(**kwargs)
    except ObjectDoesNotExist:
        return None
    except MultipleObjectsReturned:
        raise Exception()
    except Exception as e:
        raise e


@logger
def needed_stickers(request, user_id):
    '''
    Handle HTTP GET and POST methods.
    The GET operation retrieves all the needed stickers for a user.
    The POST operation reads the query string "params", parse the data and add to the user needed sticker list
    :param request:
    :param user_id:
    :return:
    '''
    try:
        user = run_secure(User.objects.get, pk=user_id)
        if not user:
            return HttpResponseNotAllowed()

        if request.method == 'GET':
            needed = run_secure(NeededStickers.objects.filter, user__id=user_id)
            return JsonResponse([i.dict() for i in needed], safe=False)

        elif request.method == 'PUT':
            stickers = request.REQUEST.get('stickers', None)
            if stickers:
                for i in stickers.split(','):
                    stick = run_secure(Sticker.objects.get, number=i)
                    if stick:
                        run_secure(NeededStickers.objects.get_or_create, sticker__number=i, user__id=user_id, defaults={'user': user, 'sticker': stick})
                return JsonResponse({}, status=201)

        elif request.method == "DELETE":
            pass
        else:
            return HttpResponseBadRequest()
    except:
        return HttpResponseBadRequest()


@logger
def duplicated_stickers(request, user_id):
    '''
    Handle HTTP GET and POST methods.
    The GET operation retrieves all the duplicated stickers for a user.
    The POST operation reads the query string "params", parse the data and add to the user needed sticker list
    :param request:
    :param user_id:
    :return:
    '''
    try:
        user = run_secure(User.objects.get, pk=user_id)
        if not user:
            return HttpResponseNotAllowed()

        if request.method == 'GET':
            needed = run_secure(DuplicatedStickers.objects.filter,user__id=user_id)
            return JsonResponse([i.dict() for i in needed], safe=False)

        elif request.method == 'PUT':
            stickers = request.REQUEST.get('stickers', None)
            if stickers:
                for i in stickers.split(','):
                    stick = run_secure(Sticker.objects.get, number=i)
                    if stick:
                        obj, created = run_secure(DuplicatedStickers.objects.get_or_create, sticker__number=i, user__id=user_id, defaults={'user': user, 'sticker': stick, 'quantity': 1})
                        if not created:
                            obj.quantity += 1
                            obj.save()
                return JsonResponse({}, status=201)

        elif request.method == "DELETE":
            sticker = request.REQUEST.get('sticker', None)
            if sticker:
                stick = run_secure(Sticker.objects.get, number=sticker)
                if stick:
                    duplicated = run_secure(DuplicatedStickers.objects.get, sticker__number=sticker, user__id=user_id)
                    if duplicated:
                        stick.delete()
            return JsonResponse({})

        else:
            return HttpResponseBadRequest()
    except:
        return HttpResponseBadRequest()


@logger
def statistics(request, user_id):
    '''
    Handle HTTP GET.
    The GET operation retrieves statistics about all the stickers for a user.
    :param request:
    :param user_id:
    :return:
    '''
    if request.method == 'GET':
        return JsonResponse(NeededStickers.calculate_stats(user_id))
    else:
        return HttpResponseBadRequest()
