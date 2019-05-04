from django.forms import ModelForm
from django import forms
from django.forms.widgets import DateInput, SelectMultiple
import logging
#added for form preview
from django.http import HttpResponseRedirect
from formtools.preview import FormPreview
#for multiple forms on page


import cfd.models as m

class CFDFormPreview(FormPreview):

    def done(self, request, cleaned_data):
        # Do something with the cleaned_data, then redirect
        # to a "success" page.
        return HttpResponseRedirect('/form/success')

class CFDForm(ModelForm):
    logger = logging.getLogger('django.server')

    class Meta:
        # DROP_DOWN_MENU_41 = (
        #     ('Transplant','Transplant'),
        #     ('Hepatitis B','Hepatitis B'),
        #     ('CMV Agents','CMV Agents'),
        #     ('HIV','HIV'),
        #     ('Anticoagulants','Anticoagulants'),
        #     ('Hepatitis C','Hepatitis C'),
        #     ('PCSK9','PCSK9')
        #     )

        model = m.cfd
        fields = '__all__'
        error_css_class = 'error'
        required_css_class = 'required'
        widgets = {
            'START_DATE': DateInput(attrs={'class': 'datepicker'}),
            'END_DATE': DateInput(attrs={'class': 'datepicker'}),
            # 'NON_SPC_CLASSES': forms.SelectMultiple(choices=DROP_DOWN_MENU_41),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("START_DATE")
        end_date = cleaned_data.get("END_DATE")

        if start_date and end_date:
            # Only do something if both fields are valid so far.
            raise forms.ValidationError(
                "The Contract Start Date must be earlier than the Contract End Date."
            )
            if start_date > end_date:
                pass

