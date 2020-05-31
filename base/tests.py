import unittest
from django.urls import reverse
from django.test import Client


class BaseTestCase(unittest.TestCase):

    def test_landing(self):
        client = Client()
        response = client.get(reverse('landing'))
        self.assertEqual(response.status_code, 200)
