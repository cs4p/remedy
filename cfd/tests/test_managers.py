from datetime import date

from django.test import TestCase

import reversion
from reversion.models import Version

from cfd.models import cfd, client

class HistoryManagerTest(TestCase):
    def setUp(self):
        client1 = client.objects.create(CLIENT_NAME='Test Client')
        client2 = client.objects.create(CLIENT_NAME='Test Client 2')

        cfd.objects.create(CLIENT=client1, START_DATE=date(2019,10,1), END_DATE=date(2019,10,10))
        cfd.objects.create(CLIENT=client1, START_DATE=date(2020,10,11), END_DATE=date(2020,11,10))
        cfd.objects.create(CLIENT=client2, START_DATE=date(2021,10,21), END_DATE=date(2021,11,20))

        for contract in cfd.objects.all():
            with reversion.create_revision():
                contract.START_DATE = date(contract.START_DATE.year + 1, 1, 1)
                contract.END_DATE = date(contract.END_DATE.year + 1, 1, 1)
                
                reversion.set_comment(f"Changed {str(contract)}")
                contract.save()

    def test_all_record_logs(self):
        contract = cfd.objects.first()
        
        logs = cfd.history.all_record_logs(contract)

        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0].revision.comment, f"Changed {str(contract)}")

    def test_filter_record_logs(self):
        contract = cfd.objects.first()

        version = cfd.history.filter_record_logs(contract, pk=1).get()
        
        self.assertEqual(version.id, 1)
        self.assertEqual(version._object_version.object.id, contract.id)