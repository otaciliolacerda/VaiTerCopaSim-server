from views import *
from django.http import JsonResponse
from django.test import TestCase, RequestFactory


def json(obj):
    return JsonResponse([i.dict() for i in obj], safe=False).content


class RequestTestHelper():

    def __init__(self, url, token):
        self.factory = RequestFactory()
        self.url = '/api/v1/sticker/needed/'
        self.token = token

    def get_request(self, method, data, is_query=False):
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
        self.user, self.token = seed(True)
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

        request = self.helper.get_request('get', {})
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
        self.user, self.token = seed(True)
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

        request = self.helper.get_request('get', {})
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
        self.user, self.token = seed(True)
        self.helper = RequestTestHelper('/api/v1/sticker/statistics/', self.token)

    def test_get_duplicated_stickers(self):
        sticker = Sticker.objects.get(number='L1')

        NeededStickers(sticker=sticker, user=self.user).save()

        request = self.helper.get_request('get', {})
        response = statistics(request)

        stats = NeededStickers.calculate_stats(self.user.id)

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
