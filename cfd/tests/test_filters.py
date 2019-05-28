from datetime import date

from django.urls import reverse
from django.test import TestCase
from django.utils import timezone
from django.forms import formset_factory

from cfd.forms import CFDForm, CFDFormset
from cfd.templatetags.filters import ( 
    get_key, get_index, get_field_data, get_form_metadata 
)

class FiltersTest(TestCase):
    def setUp(self):
        Formset = formset_factory(CFDForm, formset=CFDFormset, extra=3)
        self.formset = Formset()

    def test_get_field_data(self):
        pass

    def test_get_index(self):
        items = [1,2,3]

        for index, item in enumerate(items):
            self.assertEqual(get_index(items, index), item)

    def test_get_key(self):
        items = { 'key1' : 1, 'key2' : 2}

        self.assertEqual(get_key(items, 'key1'), 1)
        self.assertEqual(get_key(items, 'key2'), 2)
        self.assertEqual(get_key(items, 'key3'), "")

    def test_get_form_metadata(self):
        counter = 1
        
        metadata = get_form_metadata(self.formset, counter)
        expected_metadata = {
            'index' : 1,
            'first' : False,
            'last' : False,
            'extra' : True
        }

        self.assertEqual(metadata, expected_metadata)

        counter = 2
        
        metadata = get_form_metadata(self.formset, counter)
        expected_metadata = {
            'index' : 2,
            'first' : False,
            'last' : True,
            'extra' : True
        }

        self.assertEqual(metadata, expected_metadata)

        self.assertRaises(ValueError, lambda : get_form_metadata(self.formset, 4))