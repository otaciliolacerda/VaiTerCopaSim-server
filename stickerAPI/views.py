# -*- coding: utf-8 -*-

import logging
import sys
from json import JSONEncoder
from models import *
from django.http import JsonResponse as InnerJsonResponse
from django.http import HttpResponseBadRequest
from django.db.models.base import ModelBase
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from oauth2_provider.decorators import protected_resource


log = logging.getLogger("[VaiTerCopaSim]")
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)


class MyEncoder(JSONEncoder):
    def default(self, o):
        try:
            iterable = iter(o)
        except TypeError:
            pass
        else:
            return list(iterable)

        # this handlers Models
        try:
            isinstance(o.__class__,ModelBase)
        except Exception:
            pass
        else:
            #from django.utils.encoding import force_text
            return o.dict()

        return super(JSONEncoder, self).default(o)


def JsonResponse(data, safe=True, status=200):
    '''
    That's looks dirty but is intended to be a simple wrapper for the JsonResponse
    :param data:
    :param safe:
    :return:
    '''
    return InnerJsonResponse(data, safe=safe, encoder=MyEncoder, status=status)


def logger(fn):
    '''
    Decorator function to log all view operations
    '''
    def inner(*args, **kwargs):
        name = str(fn.__name__)
        method = args[0].method
        log.debug('%s received an HTTP %s' % (name, method))

        response = fn(*args, **kwargs)

        if response:
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
@protected_resource()
def needed_stickers(request):
    '''
    Handle HTTP GET and POST methods.
    The GET operation retrieves all the needed stickers for a user.
    The POST operation reads the query string "params", parse the data and add to the user needed sticker list
    :param request:
    :param user_id:
    :return:
    '''
    try:
        user = request.resource_owner

        if request.method == 'GET':
            needed = run_secure(NeededStickers.objects.filter, user__id=user.id)
            return JsonResponse(needed, safe=False)

        elif request.method == 'PUT':
            stickers = request.POST.get('stickers', None)
            if stickers:
                for i in stickers.split(','):
                    stick = run_secure(Sticker.objects.get, number=i)
                    if stick:
                        run_secure(NeededStickers.objects.get_or_create, sticker__number=i, user__id=user.id, defaults={'user': user, 'sticker': stick})
                return JsonResponse({}, status=201)

        elif request.method == "DELETE":
            sticker = request.GET.get('sticker', None)
            if sticker:
                stick = run_secure(Sticker.objects.get, number=sticker)
                if stick:
                    needed = run_secure(NeededStickers.objects.get, sticker__number=sticker, user__id=user.id)
                    if needed:
                        needed.delete()
            return JsonResponse({})

        else:
            return HttpResponseBadRequest()
    except:
        print 'ERROR'
        return HttpResponseBadRequest()


@logger
@protected_resource()
def duplicated_stickers(request):
    '''
    Handle HTTP GET and POST methods.
    The GET operation retrieves all the duplicated stickers for a user.
    The POST operation reads the query string "params", parse the data and add to the user needed sticker list
    :param request:
    :param user_id:
    :return:
    '''
    try:
        user = request.resource_owner

        if request.method == 'GET':
            duplicated = run_secure(DuplicatedStickers.objects.filter, user__id=user.id)
            return JsonResponse(duplicated, safe=False)

        elif request.method == 'PUT':
            stickers = request.POST.get('stickers', None)
            if stickers:
                for i in stickers.split(','):
                    stick = run_secure(Sticker.objects.get, number=i)
                    if stick:
                        obj, created = run_secure(DuplicatedStickers.objects.get_or_create, sticker__number=i, user__id=user.id, defaults={'user': user, 'sticker': stick, 'quantity': 1})
                        if not created:
                            obj.quantity += 1
                            obj.save()
                return JsonResponse({}, status=201)

        elif request.method == "DELETE":
            sticker = request.GET.get('sticker', None)
            if sticker:
                stick = run_secure(Sticker.objects.get, number=sticker)
                if stick:
                    duplicated = run_secure(DuplicatedStickers.objects.get, sticker__number=sticker, user__id=user.id)
                    if duplicated:
                        if duplicated.quantity > 1:
                            duplicated.quantity -= 1
                            duplicated.save()
                        else:
                            duplicated.delete()
            return JsonResponse({})

        else:
            return HttpResponseBadRequest()
    except:
        return HttpResponseBadRequest()


@logger
@protected_resource()
def statistics(request):
    '''
    Handle HTTP GET.
    The GET operation retrieves statistics about all the stickers for a user.
    :param request:
    :param user_id:
    :return:
    '''
    user = request.resource_owner
    if request.method == 'GET':
        return JsonResponse(calculate_stats(user.id))
    else:
        return HttpResponseBadRequest()


from django.db.models import Count
from social.apps.django_app.default.models import UserSocialAuth

@logger
@protected_resource()
def search(request):
    '''
    Handle HTTP GET.
    The GET operation retrieves users
    :param request:
    :param user_id:
    :return:
    '''
    user = request.resource_owner
    if request.method == 'GET':

        #needed stickers
        needed = Sticker.objects.filter(neededstickers__user__id=user.id)

        #This ugly query is the same as the both queries in comments. Load all the duplicated stickers in
        #memory and then group by user would impact performance
        offers_by_user = DuplicatedStickers.objects.exclude(user__id=user.id).filter(sticker__in=needed) \
            .values('user_id').annotate(total=Count('sticker_id')).order_by('-total')

        #all the offers for the current needed
        #offers = DuplicatedStickers.objects.exclude(user__id=user.id).filter(sticker__in=needed)

        #groups by user and calculates the quantity of offers of each user
        #offers_by_user = offers.values('user_id').annotate(total=Count('sticker_id')).order_by('-total')

        response = []
        for result in offers_by_user:
            user = UserSocialAuth.objects.get(user__id=result.get('user_id'))
            response.append({
                'uid': user.uid,
                'id': user.user.id,
                'name': '%s %s' % (user.user.first_name, user.user.last_name),
                'duplicated_count': result.get('total')
            })

        return JsonResponse(response, safe=False)
    else:
        return HttpResponseBadRequest()


@logger
@protected_resource()
def compare(request):
    '''
    Handle HTTP GET.
    The GET operation retrieves users
    :param request:
    :param user_id:
    :return:
    '''
    current_user = request.resource_owner #Model: User
    other_user_id = request.GET.get('user_id', None)
    other_user = UserSocialAuth.objects.get(user__id=other_user_id)

    #get other user duplicated and needed
    other_user_duplicated = DuplicatedStickers.objects.filter(user__id=other_user.user.id).order_by('sticker__order')
    other_user_needed = NeededStickers.objects.filter(user__id=other_user.user.id).order_by('sticker__order')

    #get the stickers of interest from the other user to the current user
    numbers = [i.sticker.number for i in DuplicatedStickers.objects.filter(user__id=current_user.id)]
    my_dupes_of_interest = other_user_needed.filter(sticker__number__in=numbers).order_by('sticker__order')

    #get the stickers of interest from the current user to the other user
    numbers = [i.sticker.number for i in other_user_duplicated]
    current_user_needed = NeededStickers.objects.filter(user__id=current_user.id)
    of_my_interest = current_user_needed.filter(sticker__number__in=numbers).order_by('sticker__order')

    response = {
        'other_user': {
            'id': other_user.user.id,
            'uid': other_user.uid,
            'name': '%s %s' % (other_user.user.first_name,other_user.user.last_name)
        },
        'my_interest': of_my_interest,
        'other_interest': my_dupes_of_interest,
        'other_duplicated': other_user_duplicated,
        'other_needed': other_user_needed,
        'other_stats': calculate_stats(other_user.user.id),
    }

    return JsonResponse(response, safe=False)


def calculate_stats(user_id):
    missing = NeededStickers.objects.filter(user__id=user_id).order_by('sticker__order')

    stats = {'collected': 649 - missing.count(), 'missing': missing.count(), 'teams': {}}

    teams = [u'Especiais', u'Estádios', u'Brasil', u'Croácia', u'México', u'Camarões', u'Espanha', u'Holanda', u'Chile',
             'Austrália', u'Colômbia', u'Grécia', u'Costa do Marfim', u'Japão', u'Uruguai', u'Costa Rica',
             'Inglaterra', u'Itália', u'Suiça', u'Equador', u'França', u'Honduras', u'Argentina' ,
             'Bósnia Herzegovina', u'Irã', u'Nigéria', u'Alemanha', u'Portugal', u'Gana', u'Estados Unidos',
             'Bélgica', u'Algéria', u'Rússia', u'Coréia', u'Propaganda']

    for team in teams:
        stats['teams'][team] = len([i for i in missing if i.sticker.team == team])

    return stats