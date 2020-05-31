import unittest
from django.urls import reverse
from django.test import Client


class UserTestCase(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def test_signup(self):
        response = self.client.get(reverse('users:signup'))
        self.assertEqual(response.status_code, 200)

    def test_signin(self):
        response = self.client.get(reverse('users:signin'))
        self.assertEqual(response.status_code, 200)

    def test_reset_password(self):
        response = self.client.get(reverse('users:reset-pass'))
        self.assertEqual(response.status_code, 200)
