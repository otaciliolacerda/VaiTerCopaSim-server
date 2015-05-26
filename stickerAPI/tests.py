from django.test import TestCase
from django.test import Client
from views import *
from django.http import JsonResponse


def json(obj):
    return JsonResponse([i.dict() for i in obj], safe=False).content


class NeededStickersTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        seed()

    def test_put_needed_stickers(self):
        client = Client()
        response = client.put('/api/v1/sticker/1/needed/?stickers=1,2,3')

        needed = NeededStickers.objects.all()

        self.assertEqual(len(needed), 3)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.resolver_match.func, needed_stickers)

    def test_get_needed_stickers(self):
        client = Client()
        client.put('/api/v1/sticker/1/needed/?stickers=1,2,3')

        response = client.get('/api/v1/sticker/1/needed/')

        needed = NeededStickers.objects.all()

        self.assertEqual(len(needed), 3)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json(needed), response.content)
        self.assertEqual(response.resolver_match.func, needed_stickers)

    def test_put_should_ignore_invalid_needed_stickers(self):
        client = Client()
        response = client.put('/api/v1/sticker/1/needed/?stickers=1,1,2')

        needed = NeededStickers.objects.all()

        self.assertEqual(len(needed), 2)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.resolver_match.func, needed_stickers)

    def test_should_throw_error_if_user_is_invalid(self):
        client = Client()
        response = client.put('/api/v1/sticker/2/needed/?stickers=1')

        needed = NeededStickers.objects.all()

        self.assertEqual(len(needed), 0)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.resolver_match.func, needed_stickers)


class DuplicatedStickersTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        seed()

    def test_put_duplicated_stickers(self):
        client = Client()
        response = client.put('/api/v1/sticker/1/duplicated/?stickers=1,2,3')

        duplicated = DuplicatedStickers.objects.all()

        self.assertEqual(len(duplicated), 3)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.resolver_match.func, duplicated_stickers)

    def test_get_duplicated_stickers(self):
        client = Client()
        client.put('/api/v1/sticker/1/duplicated/?stickers=1,2,3')

        response = client.get('/api/v1/sticker/1/duplicated/')

        duplicated = DuplicatedStickers.objects.all()

        self.assertEqual(len(duplicated), 3)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json(duplicated), response.content)
        self.assertEqual(response.resolver_match.func, duplicated_stickers)

    def test_put_should_increment_existing_duplicated_stickers(self):
        client = Client()
        response = client.put('/api/v1/sticker/1/duplicated/?stickers=1,1,1')

        duplicated = DuplicatedStickers.objects.all()

        self.assertEqual(len(duplicated), 1)
        self.assertEqual(duplicated[0].quantity, 3)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.resolver_match.func, duplicated_stickers)

    def test_should_throw_error_if_user_is_invalid(self):
        client = Client()
        response = client.put('/api/v1/sticker/2/duplicated/?stickers=1')

        duplicated = DuplicatedStickers.objects.all()

        self.assertEqual(len(duplicated), 0)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.resolver_match.func, duplicated_stickers)

