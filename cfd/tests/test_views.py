from datetime import date

from django.urls import reverse
from django.forms import formset_factory
from django.test import Client, TestCase, RequestFactory

import reversion

from cfd.models import cfd, client, User
from cfd.forms import CFDForm, CFDSearchForm
from cfd.views import RETAIL_90_MAIL_RATES_B_LIST, RETAIL_90_MAIL_RATES_G_LIST

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
        self.assertEqual(response.url, f"/admin/login?next={self.url}")

    def test_unauthenticated_post(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/admin/login?next={self.url}")

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
        self.assertEqual(response.url, f"/admin/login?next={self.url}")

    def test_unauthenticated_post(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/admin/login?next={self.url}")

    def test_get(self):
        self.client.login(username='user', password='pass')
        
        response = self.client.get(self.url)

        self.assertTemplateUsed('template_list.html')
        self.assertEqual(response.status_code, 200)

        context = response.context

        self.assertEqual(len(context['object_list']), 1)

    def test_post(self):
        self.client.login(username='user', password='pass')

        response = self.client.post(self.url, {})

        self.assertEqual(response.status_code, 405)

    
class CFDCreateViewTest(TestCase):
    def setUp(self):
        self.url = reverse('cfd:cfd_new')

        self.client = Client()

        self.user = User.objects.create(username='user', is_superuser=True)
        self.user.set_password('pass')
        self.user.save()

        client1 = client.objects.create(CLIENT_NAME='Test Client')

    def test_unauthenticated_get(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/admin/login?next={self.url}")

    def test_unauthenticated_post(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/admin/login?next={self.url}")

    def test_get(self):
        self.client.login(username='user', password='pass')

        response = self.client.get(self.url)

        self.assertTemplateUsed('cfd_form.html')
        self.assertEqual(response.status_code, 200)        

        context = response.context

        CFDFormset = formset_factory(CFDForm, extra=3)
        
        self.assertTrue(context['create'])
        self.assertEqual(len(context['formset'].forms), 3)
        self.assertEqual(context['fieldsets'], CFDForm.Meta.fieldsets)
        self.assertEqual(context['RETAIL_90_MAIL_RATES_B_LIST'], RETAIL_90_MAIL_RATES_B_LIST)
        self.assertEqual(context['RETAIL_90_MAIL_RATES_G_LIST'], RETAIL_90_MAIL_RATES_G_LIST)
        

    def test_post(self):
        self.client.login(username='user', password='pass')

        management_form_data = {
            'form-TOTAL_FORMS' : 3,
            'form-INITIAL_FORMS' : 0,
            'form-MIN_NUM_FORMS' : 0,
            'form-MAX_NUM_FORMS' : 1000
        }

        data = {
            'CLIENT' : client.objects.first().pk,
            'CONTRACT_TYPE' : cfd.DROP_DOWN_MENU_CONTRACT_TYPE_CHOICES[0][0],
            'RETAIL_90_MAIL_RATES_B' : 'N',
            'RETAIL_90_MAIL_RATES_G' : 'N',
            'RETAIL_90_MAIL_RATES_B_DS' : 10,
            'RETAIL_90_MAIL_RATES_G_DS' : 10,
            'M_RATE_BREAKOUT' : 10
        }

        form_data = {}
        form_data.update(management_form_data)

        form = CFDForm()

        # Fills out the form with default data
        for key in form.fields.keys():
            value = form.fields[key].initial            
            
            if value:
                temp = {
                    f'form-0-{key}' : value,
                    f'form-1-{key}' : value,
                    f'form-2-{key}' : value
                }

                form_data.update(temp)
            
            elif 'Discount' in form.fields[key].label or 'Fee' in form.fields[key].label:
                temp = {
                    f'form-0-{key}' : 1,
                    f'form-1-{key}' : 1,
                    f'form-2-{key}' : 1
                }

                form_data.update(temp)

        for key in data.keys():
            temp = {
                f'form-0-{key}' : data[key],
                f'form-1-{key}' : data[key],
                f'form-2-{key}' : data[key]
            }

            form_data.update(temp)
        
        response = self.client.post(self.url, form_data)      

        # The view redirects to the list view after a 
        # successful post request  
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('cfd:cfd_list'))

        contract = cfd.objects.filter(**data).first()        
        self.assertTrue(cfd.history.all_record_logs(contract).exists())

        self.assertEqual(len(cfd.objects.filter(**data)), 3)

        response = self.client.post(self.url, management_form_data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['formset'].errors), 3)


class CFDUpdateViewTest(TestCase):
    def setUp(self):
        
        self.client = Client()

        self.user = User.objects.create(username='user', is_superuser=True)
        self.user.set_password('pass')
        self.user.save()

        client1 = client.objects.create(CLIENT_NAME='Test Client')

        contract1 = cfd.objects.create(CLIENT=client1, START_DATE=date(2019,10,1), END_DATE=date(2019,10,10))
        cfd.objects.create(CLIENT=client1, START_DATE=date(2019,10,11), END_DATE=date(2019,11,10))
        cfd.objects.create(CLIENT=client1, START_DATE=date(2019,10,21), END_DATE=date(2019,11,20))

        self.url = reverse('cfd:cfd_edit', args=[contract1.pk])

    
    def test_unauthenticated_get(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/admin/login?next={self.url}")

    def test_unauthenticated_post(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/admin/login?next={self.url}")

    def test_get(self):
        self.client.login(username='user', password='pass')

        response = self.client.get(self.url)

        self.assertTemplateUsed('cfd_form.html')
        self.assertEqual(response.status_code, 200)

        context = response.context

        CFDFormset = formset_factory(CFDForm, extra=3)
                
        self.assertEqual(len(context['formset'].forms), 3)
        self.assertEqual(context['fieldsets'], CFDForm.Meta.fieldsets)
        self.assertEqual(context['RETAIL_90_MAIL_RATES_B_LIST'], RETAIL_90_MAIL_RATES_B_LIST)
        self.assertEqual(context['RETAIL_90_MAIL_RATES_G_LIST'], RETAIL_90_MAIL_RATES_G_LIST)

        contract = cfd.objects.get(CLIENT__CLIENT_NAME='Test Client', START_DATE=date(2019,10,1))

        contracts = [contract]
        contracts.extend(contract.get_subsequent_contracts(2))

        for item in zip(context['formset'].forms, contracts):
            form, contract = item            
            for field in form.fields.keys():
                self.assertEqual(form.fields[field].initial, getattr(contract, field))

    
    def test_post(self):
        self.client.login(username='user', password='pass')

        management_form_data = {
            'form-TOTAL_FORMS' : 3,
            'form-INITIAL_FORMS' : 0,
            'form-MIN_NUM_FORMS' : 0,
            'form-MAX_NUM_FORMS' : 1000
        }

        form_data = {
            'form-0-START_DATE' : '2019-10-18',
            'form-0-END_DATE' : '2019-10-51',            
        }

        form_data.update(management_form_data)

        response = self.client.post(self.url, form_data)

        self.assertTrue(len(response.context['formset'].errors) > 0)

        form_data = {}

        form = CFDForm()
        contract = cfd.objects.first()
        contracts = [contract]
        contracts.extend(contract.get_subsequent_contracts(2))

        for field in form.fields.keys():
            if field == 'CLIENT':
                continue
            
            form_data.update({
                f'form-0-{field}' : getattr(contracts[0], field),
                f'form-1-{field}' : getattr(contracts[1], field),
                f'form-2-{field}' : getattr(contracts[2], field)
            })

        client_pk = client.objects.first().pk

        form_data.update(management_form_data)
        form_data.update({
            'form-0-START_DATE' : '2019-10-18',
            'form-0-END_DATE' : '2019-10-30',
            'form-1-START_DATE' : '2020-10-18',
            'form-1-END_DATE' : '2020-10-30',
            'form-2-START_DATE' : '2021-10-18',
            'form-2-END_DATE' : '2021-10-30',
            'form-0-RETAIL_90_MAIL_RATES_B' : 'N',
            'form-0-RETAIL_90_MAIL_RATES_G' : 'N',
            'form-1-RETAIL_90_MAIL_RATES_B' : 'N',
            'form-1-RETAIL_90_MAIL_RATES_G' : 'N',
            'form-2-RETAIL_90_MAIL_RATES_B' : 'N',
            'form-2-RETAIL_90_MAIL_RATES_G' : 'N',
            'form-0-CLIENT' : client_pk,
            'form-0-CONTRACT_TYPE' : 'TBD',
            'form-1-CLIENT' : client_pk,
            'form-1-CONTRACT_TYPE' : 'TBD',
            'form-2-CLIENT' : client_pk,
            'form-2-CONTRACT_TYPE' : 'TBD',
        })


        response = self.client.post(self.url, form_data)
        
        expected_changed_fields = [{
            'START_DATE' : True,
            'END_DATE' : True,
            'RETAIL_90_MAIL_RATES_B' : True,
            'RETAIL_90_MAIL_RATES_G' : True,
            'CONTRACT_TYPE' : True
        },{
            'START_DATE' : True,
            'END_DATE' : True,
            'RETAIL_90_MAIL_RATES_B' : True,
            'RETAIL_90_MAIL_RATES_G' : True,
            'CONTRACT_TYPE' : True
        },{
            'START_DATE' : True,
            'END_DATE' : True,
            'RETAIL_90_MAIL_RATES_B' : True,
            'RETAIL_90_MAIL_RATES_G' : True,
            'CONTRACT_TYPE' : True
        }]

        # Checks that the confirmation page came up
        self.assertTemplateUsed('cfd_confirmation.html')
        
        self.assertTrue(response.context['confirmation'])
        self.assertEqual(response.context['changed'], expected_changed_fields)

        form_data.update({ 'is_confirmation_page'  : "True" })

        response = self.client.post(self.url, form_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('cfd:cfd_list'))

        logs = cfd.history.all_record_logs(contract)
        self.assertTrue(logs.exists())    
        self.assertTrue("Changed Contract Start Date from 2019-10-01 to 2019-10-18;\n" in logs.first().revision.comment)

class CFDDeleteViewTest(TestCase):
    def setUp(self):
         
        self.client = Client()

        self.user = User.objects.create(username='user', is_superuser=True)
        self.user.set_password('pass')
        self.user.save()

        client1 = client.objects.create(CLIENT_NAME='Test Client')

        self.contract = cfd.objects.create(CLIENT=client1, START_DATE=date(2019,10,1), END_DATE=date(2019,10,10))

        self.url = reverse('cfd:cfd_delete', args=[self.contract.pk])

    def test_unauthenticated_get(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/admin/login?next={self.url}")

    def test_unauthenticated_post(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/admin/login?next={self.url}")

    def test_get(self):
        self.client.login(username='user', password='pass')

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'].pk, self.contract.pk)

    def test_post(self):
        self.client.login(username='user', password='pass')

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('cfd:cfd_list'))
        
        self.assertEqual(cfd.objects.filter(pk=self.contract.pk).count(), 0)


class CFDCopyViewTest(TestCase):
    def setUp(self):
          
        self.client = Client()

        self.user = User.objects.create(username='user', is_superuser=True)
        self.user.set_password('pass')
        self.user.save()

        client1 = client.objects.create(CLIENT_NAME='Test Client')
        self.client2 = client.objects.create(CLIENT_NAME='Other Client')

        self.contract = cfd.objects.create(CLIENT=client1, START_DATE=date(2019,10,1), END_DATE=date(2019,10,10))

        self.url = reverse('cfd:cfd_copy', args=[self.contract.pk])

    def test_unauthenticated_get(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/admin/login?next={self.url}")

    def test_unauthenticated_post(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/admin/login?next={self.url}")

    def test_get(self):
        self.client.login(username='user', password='pass')

        response = self.client.get(self.url)
        context = response.context

        self.assertTemplateUsed('cfd_form.html')
        self.assertEqual(response.status_code, 200)        

        self.assertEqual(context['form'].instance.pk, None)
        self.assertEqual(context['fieldsets'], CFDForm.Meta.fieldsets)
        self.assertEqual(context['form'].instance.START_DATE, self.contract.START_DATE)
        self.assertEqual(context['RETAIL_90_MAIL_RATES_B_LIST'], RETAIL_90_MAIL_RATES_B_LIST)
        self.assertEqual(context['RETAIL_90_MAIL_RATES_G_LIST'], RETAIL_90_MAIL_RATES_G_LIST)

    def test_post(self):
        self.client.login(username='user', password='pass')

        data = {
            'CLIENT' : self.client2.pk,
            'START_DATE' : '2019-11-11',
            'END_DATE' : '2019-12-11',
            'CONTRACT_TYPE' : 'TBD',
            'RETAIL_90_MAIL_RATES_B' : 'N',
            'RETAIL_90_MAIL_RATES_G' : 'N',
        }

        form_data = {}

        form = CFDForm()

        for field in form.fields.keys():
            value = getattr(self.contract, field)
            if field == 'CLIENT' or value in (None, ''):
                continue
            
            form_data.update({
                field : value,                
            })


        data.update(form_data)
        response = self.client.post(self.url, data)
        
        self.assertEqual(cfd.objects.count(), 2)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(cfd.objects.filter(**data).exists())        
        self.assertEqual(response.url, reverse('cfd:cfd_list'))

        new_contract = cfd.objects.get(**data)
        self.assertTrue(cfd.history.all_record_logs(new_contract).exists())
        
        
class CFDHistoryViewTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create(username='user', is_superuser=True)
        self.user.set_password('pass')
        self.user.save()

        client1 = client.objects.create(CLIENT_NAME='Test Client')        

        self.contract = cfd.objects.create(CLIENT=client1, START_DATE=date(2019,10,1), END_DATE=date(2019,10,10))

        with reversion.create_revision():                                
            reversion.set_comment("Test")
            self.contract.save()

        self.url = reverse('cfd:cfd_history', args=[self.contract.pk])

    def test_unauthenticated_get(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/admin/login?next={self.url}")

    def test_unauthenticated_post(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/admin/login?next={self.url}")

    def test_get(self):
        self.client.login(username='user', password='pass')

        response = self.client.get(self.url)
        context = response.context
        
        self.assertEqual(response.status_code, 200)        
        self.assertTemplateUsed('cfd_history.html')

        self.assertEqual(len(context['logs']), 1)
        self.assertEqual(context['record'].pk, self.contract.pk)
        
    def test_post(self):
        self.client.login(username='user', password='pass')

        response = self.client.post(self.url, {})

        self.assertEqual(response.status_code, 405)

class CFDHistoryDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create(username='user', is_superuser=True)
        self.user.set_password('pass')
        self.user.save()

        client1 = client.objects.create(CLIENT_NAME='Test Client')        
        self.client2 = client.objects.create(CLIENT_NAME='Other Client')

        self.contract = cfd.objects.create(CLIENT=client1, START_DATE=date(2019,10,1), END_DATE=date(2019,10,10))

        with reversion.create_revision():                                
            reversion.set_comment("Test")
            self.contract.START_DATE = date(2019,10,8)
            self.contract.save()

        self.log = cfd.history.all_record_logs(self.contract).first()
        self.url = reverse('cfd:cfd_history_detail', args=[self.contract.pk, self.log.pk])

    def test_unauthenticated_get(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/admin/login?next={self.url}")

    def test_unauthenticated_post(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/admin/login?next={self.url}")

    def test_get(self):
        self.client.login(username='user', password='pass')

        response = self.client.get(self.url)
        context = response.context

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('cfd_recover_form.html')
                
        self.assertEqual(context['record'].pk, self.contract.pk)
        self.assertEqual(context['version'].pk, self.log._object_version.object.pk)

    def test_post(self):
        self.client.login(username='user', password='pass')

        data = {
            'CLIENT' : self.client2.pk,
            'START_DATE' : '2019-11-11',
            'END_DATE' : '2019-12-11',
            'CONTRACT_TYPE' : 'TBD',
            'RETAIL_90_MAIL_RATES_B' : 'N',
            'RETAIL_90_MAIL_RATES_G' : 'N',
        }

        form_data = {}

        form = CFDForm()

        for field in form.fields.keys():
            value = getattr(self.contract, field)
            if field == 'CLIENT' or value in (None, ''):
                continue
            
            form_data.update({
                field : value,                
            })


        data.update(form_data)
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('cfd:cfd_list'))

        self.assertEqual(cfd.history.all_record_logs(self.contract).count(), 2)