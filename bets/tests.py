from django.test import TestCase


class TestingCI(TestCase):

    def test_1(self):
        self.assertEquals(True, True)