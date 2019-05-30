from datetime import date

from django.urls import reverse
from django.template import RequestContext
from django.test import Client, TestCase, RequestFactory

from cfd.forms import CFDSearchForm
from cfd.models import cfd, client, User

class CFDListViewTest(TestCase):
    def setUp(self):
        self.url = reverse('cfd:cfd_list')

        self.client = Client()

        self.user = User.objects.create(username='user', is_superuser=True)
        self.user.set_password('pass')
        self.user.save()

        client1 = client.objects.create(CLIENT_NAME='Test Client')
        client2 = client.objects.create(CLIENT_NAME='Other Client')

        cfd.objects.create(CLIENT=client1, START_DATE=date(2019,10,1), END_DATE=date(2019,10,10))
        cfd.objects.create(CLIENT=client1, START_DATE=date(2019,10,11), END_DATE=date(2019,11,10))
        cfd.objects.create(CLIENT=client1, START_DATE=date(2019,10,21), END_DATE=date(2019,11,20), confirmed=False)

        cfd.objects.create(CLIENT=client2, START_DATE=date(2019,10,1), END_DATE=date(2019,10,10))
        cfd.objects.create(CLIENT=client2, START_DATE=date(2019,10,1), END_DATE=date(2019,12,10), IS_TEMPLATE=True)

    def test_unauthenticated_get(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)

    def test_unauthenticated_post(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)

    def test_get(self):
        self.client.login(username='user', password='pass')
        
        response = self.client.get(self.url)

        self.assertTemplateUsed('cfd_list.html')
        self.assertEqual(response.status_code, 200)        

        context = response.context

        self.assertEqual(len(context['object_list']), 3)
        self.assertEqual(len(context['templates']), 1)
        self.assertEqual(len(context['pending']), 1)

        self.assertTrue(isinstance(context['form'], CFDSearchForm))

    def test_post(self):
        self.client.login(username='user', password='pass')

        form_data = {
            'client_name' : 'Test',
            'start_date' : '2019-10-18',
            'end_date' : '2019-10-30'
        }
        
        response = self.client.post(self.url, form_data)

        self.assertTemplateUsed('cfd_list.html')
        self.assertEqual(response.status_code, 200)

        context = response.context

        self.assertEqual(len(context['object_list']), 1)
        self.assertEqual(len(context['templates']), 0)
        self.assertEqual(len(context['pending']), 1)

        self.assertTrue(isinstance(context['form'], CFDSearchForm))


class TemplateListViewTest(TestCase):
    def setUp(self):
        self.url = reverse('cfd:template_list')

        self.client = Client()

        self.user = User.objects.create(username='user', is_superuser=True)
        self.user.set_password('pass')
        self.user.save()

        client1 = client.objects.create(CLIENT_NAME='Test Client')

        cfd.objects.create(CLIENT=client1, START_DATE=date(2019,10,1), END_DATE=date(2019,10,10))
        cfd.objects.create(CLIENT=client1, START_DATE=date(2019,10,1), END_DATE=date(2019,12,10), IS_TEMPLATE=True)

    def test_unauthenticated_get(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)

    def test_unauthenticated_post(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)

    def test_get(self):
        self.client.login(username='user', password='pass')
        
        response = self.client.get(self.url)

        self.assertTemplateUsed('template_list.html')
        self.assertEqual(response.status_code, 200)

        context = response.context

        self.assertEqual(len(context['object_list']), 1)