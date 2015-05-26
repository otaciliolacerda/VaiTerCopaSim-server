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
        print user
        if not user:
            return HttpResponseNotAllowed()

        if request.method == 'GET':
            needed = run_secure(NeededStickers.objects.filter, user__id=user_id)
            return JsonResponse([i.dict() for i in needed], safe=False, status=200)

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
    if request.method == 'GET':
        needed = DuplicatedStickers.objects.filter(user__id=user_id)
        return JsonResponse([i.dict() for i in needed], safe=False)
    elif request.method == 'PUT':
        stickers = request.REQUEST.get('stickers', None)
        if stickers:
            for i in stickers.split(','):
                stick = None
                try:
                    user = User.objects.get(pk=user_id)
                    stick = Sticker.objects.get(number=i)
                    dupli = DuplicatedStickers.objects.get(sticker__number=i, user__id=user_id)
                    dupli.quantity += 1
                    dupli.save()
                except ObjectDoesNotExist:
                    DuplicatedStickers(user=user, sticker=stick, quantity=1).save()
                    continue
            return JsonResponse({})
        else:
            return HttpResponseBadRequest({})
    elif request.method == "DELETE":
        pass
    else:
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
