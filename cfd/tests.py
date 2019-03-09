from django.test import TestCase
from cfd.models import client, cfd
from django.utils import timezone
from django.urls import reverse
from cfd.views import PostsForm
#from whatever.forms import WhateverForm

# Create your tests here.

# models test
class ClientTest(TestCase):

    def create_client(self, CLIENT_NAME="A Test Client"):
        return client.objects.create(CLIENT_NAME=CLIENT_NAME)

    def test_client_creation(self):
        c = self.create_client()
        self.assertTrue(isinstance(c, client))
        #self.assertEqual(c.__unicode__(), c.CLIENT_NAME)

class cfdTest(TestCase):

    def create_cfd(self):
        return cfd.objects.create(CLIENT_id=1)

    def test_cfd_creation(self):
        c = self.create_cfd()
        self.assertTrue(isinstance(c, cfd))
        #self.assertEqual(c.__unicode__(), c.CLIENT_id)

    # views (uses reverse)

    def test_cfd_list_view(self):
        #c = self.create_cfd()
        url = reverse('cfd.views.PostForm.post_list')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        #self.assertIn(c.title, resp.content)