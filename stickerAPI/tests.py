from views import *
from django.http import QueryDict
from django.test import TestCase, RequestFactory


def json(obj):
    #JsonResponse from models
    return JsonResponse(obj, safe=False).content


class RequestTestHelper():

    def __init__(self, url, token):
        self.factory = RequestFactory()
        self.url = '/api/v1/sticker/needed/'
        self.token = token

    def get_request(self, method, data={}, is_query=False):
        fn = getattr(self.factory, method)
        request = None
        if is_query:
            self.url += '?'
            for key, value in data.iteritems():
                self.url += str(key) + '=' + str(value)

            print self.url
            request = fn(self.url)
        else:
            request = fn(self.url, data)

        #Put the token in the headers for all requests
        request.META['HTTP_AUTHORIZATION'] = 'Bearer %s' % self.token.token

        #Apply the middleware behaviour
        post = QueryDict(mutable=True)
        post.update(data)
        request.POST = post

        return request


class NeededStickersTests(TestCase):

    def setUp(self):
        # Set up data for the whole TestCase
        users = seed(True)
        self.user, self.token = users[0].get('user'), users[0].get('token')
        self.helper = RequestTestHelper('/api/v1/sticker/needed/', self.token)

    def test_put_needed_stickers(self):
        data = {'stickers': '1,2,3'}

        request = self.helper.get_request('put', data)
        response = needed_stickers(request)

        needed = NeededStickers.objects.all()

        self.assertEqual(len(needed), 3)
        self.assertEqual(response.status_code, 201)

    def test_get_needed_stickers(self):
        data = {'stickers': '1,2,3'}

        request = self.helper.get_request('put', data)
        needed_stickers(request)

        request = self.helper.get_request('get')
        response = needed_stickers(request)

        needed = NeededStickers.objects.all()

        self.assertEqual(len(needed), 3)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json(needed), response.content)

    def test_put_should_ignore_invalid_needed_stickers(self):
        data = {'stickers': '1,1,2'}

        request = self.helper.get_request('put', data)
        response = needed_stickers(request)

        needed = NeededStickers.objects.all()

        self.assertEqual(len(needed), 2)
        self.assertEqual(response.status_code, 201)

    def test_delete_needed_stickers(self):
        data = {'stickers': '1,2,3'}

        request = self.helper.get_request('put', data)
        response = needed_stickers(request)

        needed = NeededStickers.objects.all()

        self.assertEqual(len(needed), 3)
        self.assertEqual(response.status_code, 201)

        #Now deleting one of the created stickers
        data = {'sticker': '2'}

        request = self.helper.get_request('delete', data, is_query=True)
        response = needed_stickers(request)

        needed = NeededStickers.objects.all()

        self.assertEqual(len(needed), 2)
        self.assertEqual(response.status_code, 200)


class DuplicatedStickersTests(TestCase):

    def setUp(self):
        # Set up data for the whole TestCase
        users = seed(True)
        self.user, self.token = users[0].get('user'), users[0].get('token')
        self.helper = RequestTestHelper('/api/v1/sticker/duplicated/', self.token)

    def test_put_duplicated_stickers(self):
        data = {'stickers': '1,2,3'}
        request = self.helper.get_request('put', data)
        response = duplicated_stickers(request)

        duplicated = DuplicatedStickers.objects.all()

        self.assertEqual(len(duplicated), 3)
        self.assertEqual(response.status_code, 201)

    def test_get_duplicated_stickers(self):
        data = {'stickers': '1,2,3'}
        request = self.helper.get_request('put', data)
        duplicated_stickers(request)

        request = self.helper.get_request('get')
        response = duplicated_stickers(request)

        duplicated = DuplicatedStickers.objects.all()

        self.assertEqual(len(duplicated), 3)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json(duplicated), response.content)

    def test_put_should_increment_existing_duplicated_stickers(self):
        data = {'stickers': '1,1,1'}
        request = self.helper.get_request('put', data)
        response = duplicated_stickers(request)

        duplicated = DuplicatedStickers.objects.all()

        self.assertEqual(len(duplicated), 1)
        self.assertEqual(duplicated[0].quantity, 3)
        self.assertEqual(response.status_code, 201)

    def test_delete_duplicated_stickers(self):
        data = {'stickers': '1,2,3'}
        request = self.helper.get_request('put', data)
        response = duplicated_stickers(request)

        duplicated = DuplicatedStickers.objects.all()

        self.assertEqual(len(duplicated), 3)
        self.assertEqual(response.status_code, 201)

        #Now deleting one of the created stickers
        data = {'sticker': '2'}
        request = self.helper.get_request('delete', data, is_query=True)
        response = duplicated_stickers(request)

        duplicated = DuplicatedStickers.objects.all()

        self.assertEqual(len(duplicated), 2)
        self.assertEqual(response.status_code, 200)

    def test_delete_duplicated_stickers_should_decrease_quantity(self):
        data = {'stickers': '1,1,1'}
        request = self.helper.get_request('put', data)
        response = duplicated_stickers(request)

        duplicated = DuplicatedStickers.objects.all()

        self.assertEqual(len(duplicated), 1)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(duplicated[0].quantity, 3)

        #Now deleting one of the created stickers
        data = {'sticker': '1'}
        request = self.helper.get_request('delete', data, is_query=True)
        response = duplicated_stickers(request)

        duplicated = DuplicatedStickers.objects.all()

        self.assertEqual(len(duplicated), 1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(duplicated[0].quantity, 2)


class StatisticsTests(TestCase):

    def setUp(self):
        # Set up data for the whole TestCase
        users = seed(True)
        self.user, self.token = users[0].get('user'), users[0].get('token')
        self.helper = RequestTestHelper('/api/v1/sticker/statistics/', self.token)

    def test_get_statistics(self):
        sticker = Sticker.objects.get(number='L1')

        NeededStickers(sticker=sticker, user=self.user).save()

        request = self.helper.get_request('get')
        response = statistics(request)

        stats = calculate_stats(self.user.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(JsonResponse(stats).content, response.content)

        #In this scenario we have only one sticker missing (number 'L1' - advertisement category) so we should have
        #only 1 missing and 648 collected
        self.assertEqual(stats['collected'], 648)
        self.assertEqual(stats['missing'], 1)
        for key, value in stats['teams'].iteritems():
            if key == 'Propaganda':
                self.assertEqual(value, 1)
            else:
                self.assertEqual(value, 0)


class SearchTests(TestCase):

    def setUp(self):
        # Set up data for the whole TestCase
        users = seed(True, number_of_users=2)
        self.user, self.token = users[0].get('user'), users[0].get('token')
        self.user2, self.token2 = users[1].get('user'), users[1].get('token')

        #Setup Data for this test
        #Stickers 1-10 (numbers) will be used in this test
        stickers = Sticker.objects.filter(number__in=range(1,11)).order_by('id')
        #self.user needs stickers 1-5 (number) and has duplicated the 6-10 (number)
        for i in range(0,5):
            NeededStickers.objects.create(user=self.user, sticker=stickers[i])
            DuplicatedStickers.objects.create(user=self.user, sticker=stickers[9-i], quantity=1)

        #self.user2 needs sticker 3,4,5,6 and 7 and has duplicated the 1,2,8,9 and 10
        #REMINDER: the values in the duple are the indexes not the sticker number
        self.other_needed = [NeededStickers.objects.create(user=self.user2, sticker=stickers[i]) for i in (2, 3, 4, 5, 6)]
        self.other_duplicated = [DuplicatedStickers.objects.create(user=self.user2, sticker=stickers[i], quantity=1) for i in (0, 1, 7, 8, 9)]

        self.helper = RequestTestHelper('/api/v1/search/', self.token)

    def test_search(self):
        request = self.helper.get_request('get')
        response = search(request)

        data = [
            {
                'uid': str(self.user2.id),
                'id': self.user2.id,
                'name': '%s %s' % (self.user2.first_name, self.user2.last_name),
                'duplicated_count': 2
            }
        ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(JsonResponse(data, safe=False).content, response.content)


class CompareTests(TestCase):

    def setUp(self):
        # Set up data for the whole TestCase
        users = seed(True, number_of_users=2)
        self.user, self.token = users[0].get('user'), users[0].get('token')
        self.user2, self.token2 = users[1].get('user'), users[1].get('token')

        #Setup Data for this test
        #Stickers 1-10 (numbers) will be used in this test
        stickers = Sticker.objects.filter(number__in=range(1,11)).order_by('id')
        #self.user needs stickers 1-5 (number) and has duplicated the 6-10 (number)
        for i in range(0,5):
            NeededStickers.objects.create(user=self.user, sticker=stickers[i])
            DuplicatedStickers.objects.create(user=self.user, sticker=stickers[9-i], quantity=1)

        #self.user2 needs sticker 3,4,5,6 and 7 and has duplicated the 1,2,8,9 and 10
        #REMINDER: the values in the duple are the indexes not the sticker number
        self.other_needed = [NeededStickers.objects.create(user=self.user2, sticker=stickers[i]) for i in (2, 3, 4, 5, 6)]
        self.other_duplicated = [DuplicatedStickers.objects.create(user=self.user2, sticker=stickers[i], quantity=1) for i in (0, 1, 7, 8, 9)]

        #Given the scenario self.user is interested in 1 and 2 from self.user2 nad self.user2 is interested in
        #6 and 7 from self.user1
        self.user_interest = Sticker.objects.filter(number__in=(1, 2))
        self.user2_interest = Sticker.objects.filter(number__in=(6, 7))

        self.helper = RequestTestHelper('/api/v1/compare/', self.token)

    def test_compare(self):
        request = self.helper.get_request('get', {"user_id": self.user2.id}, is_query=True)
        response = compare(request)

        data = {
            'other_user': {
                'id': self.user2.id,
                'uid': str(self.user2.id),
                'name': '%s %s' % (self.user2.first_name, self.user2.last_name)
            },
            'my_interest': self.user_interest,
            'other_interest': self.user2_interest,
            'other_duplicated': self.other_duplicated,
            'other_needed': self.other_needed,
            'other_stats': calculate_stats(self.user2.id),
            }

        self.assertEqual(response.status_code, 200)

        #Since the response has special characters it needs to be converted to unicode before compare
        unicode_data = unicode(JsonResponse(data).content, "utf-8")
        unicode_response = unicode(response.content, "utf-8")
        self.assertEqual(unicode_data, unicode_response)