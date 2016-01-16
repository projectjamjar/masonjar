
from django.test import TestCase

class LiloTestCase(TestCase):
    def setUp(self):
        pass

    def test_import(self):
        from lilo import Lilo
