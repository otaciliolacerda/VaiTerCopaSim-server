from django.test import TestCase
from seed import seed

class ViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        seed()


    def test1(self):
        pass