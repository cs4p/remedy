from datetime import date

from django.urls import reverse
from django.test import TestCase
from django.utils import timezone

from cfd.forms import CFDForm
from cfd.models import cfd, client

class CFDTest(TestCase):
    def setUp(self):
        client1 = client.objects.create(CLIENT_NAME='Test Client')
        client2 = client.objects.create(CLIENT_NAME='Other Client')

        cfd.objects.create(CLIENT=client1, START_DATE=date(2019,10,1), END_DATE=date(2019,10,10))
        cfd.objects.create(CLIENT=client1, START_DATE=date(2019,10,11), END_DATE=date(2019,11,10))
        cfd.objects.create(CLIENT=client1, START_DATE=date(2019,10,21), END_DATE=date(2019,11,20))

        cfd.objects.create(CLIENT=client2, START_DATE=date(2019,10,1), END_DATE=date(2019,10,10))
        cfd.objects.create(CLIENT=client2, START_DATE=date(2019,10,1), END_DATE=date(2019,12,10), IS_TEMPLATE=True)

    
    def test_search(self):
        '''
        Tests if the cfd search class method returns contracts in the
        correct date range with the expected clients
        '''

        contracts = cfd.search(start_date=date(2019, 12, 1))
        expected = cfd.objects.get(CLIENT=client.objects.get(pk=2), START_DATE=date(2019,10,1), END_DATE=date(2019,12,10))
        self.assertEqual(len(contracts), 1)        
        self.assertEqual(contracts[0], expected)

        contracts = cfd.search(start_date=date(2019, 10, 1))
        self.assertEqual(len(contracts), 5)


        contracts = cfd.search(end_date=date(2019, 12, 1))        
        self.assertEqual(len(contracts), 5)        

        contracts = cfd.search(start_date=date(2019, 10, 1), end_date=date(2019,10,12))        
        self.assertEqual(len(contracts), 4)        


        contracts = cfd.search(client_name="Client")
        self.assertEqual(len(contracts), 5)

        contracts = cfd.search(client_name="Random Client")
        self.assertEqual(len(contracts), 0)

        contracts = cfd.search(client_name="Test")
        self.assertEqual(len(contracts), 3)

        contracts = cfd.search()
        self.assertEqual(len(contracts), 5)

        contracts = cfd.search(is_template=True)
        expected = cfd.objects.get(CLIENT=client.objects.get(pk=2), IS_TEMPLATE=True)
        self.assertEqual(len(contracts), 1)
        self.assertEqual(contracts[0], expected)

    def test_get_subsequent_contracts(self):
        '''
        Checks if the get_subsequent_contracts method returns the 
        closest non template contracts started after the given contract if they
        exist and fresh objects if not
        '''
        contract = cfd.objects.get(CLIENT__CLIENT_NAME='Test Client', START_DATE=date(2019,10,1))

        subsequent_contracts = contract.get_subsequent_contracts(2)
        expected = list(cfd.objects.filter(CLIENT__CLIENT_NAME='Test Client').exclude(pk=contract.pk))

        self.assertEqual(len(subsequent_contracts), 2)
        self.assertEqual(subsequent_contracts, expected)


        contract = cfd.objects.get(CLIENT__CLIENT_NAME='Other Client', START_DATE=date(2019,10,1), IS_TEMPLATE=False)
        client2 = client.objects.get(CLIENT_NAME='Other Client')

        subsequent_contracts = contract.get_subsequent_contracts(2)        

        self.assertEqual(len(subsequent_contracts), 2)

        self.assertEqual(subsequent_contracts[0].CLIENT, client2)
        self.assertEqual(subsequent_contracts[0].START_DATE.year, 2020)

        self.assertEqual(subsequent_contracts[1].CLIENT, client2)
        self.assertEqual(subsequent_contracts[1].START_DATE.year, 2021)


    def test_get_changed_fields(self):
        '''
        Checks if the get_changed_fields method returns the
        correct dicts
        '''
        client2 = client.objects.get(CLIENT_NAME='Other Client')
        contract = cfd(CLIENT=client2)

        changed_fields = contract.get_changed_fields()
        self.assertEqual(changed_fields, {})

        contract = cfd.objects.first()

        changed_fields = contract.get_changed_fields()
        self.assertEqual(changed_fields, {})

        contract.START_DATE = date(contract.START_DATE.year + 1, contract.START_DATE.month, contract.START_DATE.day)
        contract.IS_TEMPLATE = not contract.IS_TEMPLATE
        
        changed_fields = contract.get_changed_fields()
        expected_changed_fields = {
            'START_DATE' : (date(contract.START_DATE.year - 1, contract.START_DATE.month, contract.START_DATE.day), contract.START_DATE),
            'IS_TEMPLATE' : (not contract.IS_TEMPLATE, contract.IS_TEMPLATE)
        }
                
        self.assertEqual(changed_fields, expected_changed_fields)
