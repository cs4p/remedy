from datetime import date

from django.test import TestCase
from django.forms import formset_factory, ValidationError

from cfd.models import cfd, client
from cfd.forms import CFDForm, CFDFormset

class CFDFormTest(TestCase):
    def setUp(self):
        client1 = client.objects.create(CLIENT_NAME='Test Client')

        cfd.objects.create(CLIENT=client1)
        cfd.objects.create(CLIENT=client1)
        cfd.objects.create(CLIENT=client1)

        self.form = CFDForm()

    def test_init(self):
        for field in self.form.fields.keys():
            field = self.form.fields[field]
            field_css_classes = field.widget.attrs.get('class', '')
            if "Discount" in field.label:                
                self.assertTrue('discount-field' in field_css_classes)
            else:
                self.assertTrue('discount-field' not in field_css_classes)

        # Checking random discount field 
        field = self.form.fields['GUAR_GR90_EZBD_DCT']
        field_css_classes = field.widget.attrs.get('class', '')

        self.assertTrue('discount-field' in field_css_classes)

    def test_set_instance_values(self):        

        contract = cfd.objects.first()
        new_contract = cfd() 

        data = {}

        for field in self.form.fields.keys():
            data[field] = getattr(contract, field)

        form = CFDForm(data=data)
        form.is_valid()

        form.cleaned_data.update(data)

        form.set_instance_values(new_contract)

        for field in form.fields.keys():
            self.assertEqual(data[field], getattr(new_contract, field))



    def test_set_initial_values(self):
        contract = cfd.objects.first()

        form = CFDForm()

        form.set_initial_values(contract)

        for field in form.fields.keys():
            self.assertEqual(form.fields[field].initial, getattr(contract, field))


    def test_get_changed_fields(self):
        contract = cfd.objects.first()

        data = {}

        for field in self.form.fields.keys():
            data[field] = getattr(contract, field)

        data.update({
            'CONTRACT_DESCRIPTION' : 'Random Text',            
        })

        form = CFDForm(data=data)
        form.is_valid()

        form.cleaned_data.update(data)

        changed_fields = form.get_changed_fields(contract)
        expected_changed_fields = {
            'CONTRACT_DESCRIPTION' : True
        }

        self.assertEqual(changed_fields, expected_changed_fields)

