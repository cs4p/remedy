import logging

from django.forms import ModelForm
from django import forms
from django.forms.widgets import DateInput, HiddenInput, SelectMultiple
from django.http import HttpResponseRedirect

import reversion
from formtools.preview import FormPreview


import cfd.models as m

class CFDFormPreview(FormPreview):

    def done(self, request, cleaned_data):
        # Do something with the cleaned_data, then redirect
        # to a "success" page.
        return HttpResponseRedirect('/form/success')

class CFDForm(ModelForm):
    logger = logging.getLogger('django.server')

    def __init__(self, *args, **kwargs):        
        super().__init__(*args, **kwargs)
        for field in self.fields.keys():
            if "Discount" in self.fields[field].label:
                self.fields[field].widget.attrs.update({ 'class' : 'discount-field' })                

    class Meta:
        model = m.cfd
        fields = '__all__'
        error_css_class = 'error'
        required_css_class = 'required'
        widgets = {
            'START_DATE': DateInput(attrs={'class': 'datepicker'}),
            'END_DATE': DateInput(attrs={'class': 'datepicker'}),
            # 'NON_SPC_CLASSES': forms.SelectMultiple(choices=DROP_DOWN_MENU_41),
            'confirmed' : HiddenInput(attrs={ 'class' : 'confirmation_flag' })
        }
        fieldsets = (
            ('Client Information', {
                'classes': ['collapse'],
                'fields': ('CLIENT',)
            }),
            ('Contract Period', {
                'classes': ['collapse'],
                'fields': ('START_DATE', 'END_DATE')
            }),
            ('Retail', {
                'classes': ['collapse'],
                'fields': ('GUAR_BR_IZBD_DCT','GUAR_BR_EZBD_DCT','GUAR_GR_IZBD_DCT', 'GUAR_GR_EZBD_DCT','GUAR_BR_DISP_FEE','GUAR_GR_DISP_FEE','GUAR_RETAIL_ADMIN_FEE','GUAR_RETAIL_REBATE')
            }),        
            ('Retail 90', {
                'classes': ['collapse'],
                'fields': ('GUAR_BR90_IZBD_DCT','GUAR_BR90_EZBD_DCT','GUAR_GR90_IZBD_DCT','GUAR_GR90_EZBD_DCT','GUAR_BR90_DISP_FEE','GUAR_GR90_DISP_FEE','GUAR_R90_ADMIN_FEE')
            }),
            ('Mail/Retail at Mail Rates', {
                'classes': ['collapse'],
                'fields': ('GUAR_BM_IZBD_DCT','GUAR_BM_EZBD_DCT','GUAR_GM_IZBD_DCT','GUAR_GM_EZBD_DCT','GUAR_BM_DISP_FEE','GUAR_GM_DISP_FEE','GUAR_MAIL_ADMIN_FEE')
            }),
            ('Specialty', { 
                'classes': ['collapse'],
                'fields': ('GUAR_SPC_BR_DCT','GUAR_SPC_GR_DCT','GUAR_SPC_BR_DISP_FEE','GUAR_SPC_GR_DISP_FEE','GUAR_SPC_RETAIL_ADMIN_FEE','GUAR_SPC_SRX_B_DCT','GUAR_SPC_SRX_G_DCT','GUAR_SPC_G_SRX_DISP_FEE','GUAR_SPC_B_SRX_DISP_FEE','GUAR_SPC_SRX_ADMIN_FEE')}),
            ('PBM Client Credits', {
                'classes': ['collapse'],
                'fields': ('IE_SSG','IE_ZBD','IE_UAC','IE_GENERICS_UNDER_EXCLUSIVITY','IE_AUTHORIZED_GENERICS','IE_PATENT_LITIGATED_GENERICS','IE_MAC_GENERICS','IE_NON_MAC_GENERICS','IE_MAC_BRANDS','IE_ADJUSTMENTS','IE_COB_SECONDARY_CLAIMS','IE_DMR_CLAIMS','IE_EXCLUDED_PROVIDERS','IE_REJECTS','IE_REVERSALS','IE_SUBROGATION','IE_NON_DRUG_ITEMS','IE_OTC','IE_PRICING_ERROR_THRESHOLDS','IE_DAW_5','IE_COMPOUNDS','M_RATES_APPLY_TO_ALL_M','M_RATE_BREAKOUT','LDD_DISC','LDD_REBATE','BIOSIMILAR_DISC','OBSOLETE_NDCS')}),
            ('Other', {
                'classes' : ['collapse'],
                'fields' : ('CONTRACT_TYPE', 'GUAR_MAIL_REBATE', 'GUAR_R90_REBATE', 'GUAR_SPC_M_REBATE', 'GUAR_SPC_R_REBATE', 'RETAIL_90_MAIL_RATES_B', 'RETAIL_90_MAIL_RATES_B_DS',
                'RETAIL_90_MAIL_RATES_G', 'RETAIL_90_MAIL_RATES_G_DS', 'RETAIL_REBATE_TYPE', 'RETAIL_SPC_REBATE_TYPE', 'MAIL_REBATE_TYPE', 'MAIL_SPC_REBATE_TYPE', 'R90_REBATE_TYPE',                
                )
            }),
            ('Hidden', {
                    'classes' : ['hidden'],
                    'fields' : ('confirmed',)
            })
        )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("START_DATE")
        end_date = cleaned_data.get("END_DATE")

        if start_date and end_date:
            # Only do something if both fields are valid so far.            
            if start_date >= end_date:
                raise forms.ValidationError(
                "The Contract Start Date must be earlier than the Contract End Date."
            )
        #TODO: The user should not be able to create a new contract that overlaps an existing contract for the same client. If this error condition is found then the user should be given the option to update the start or end date of the existing contract to correct the error.
        
        return cleaned_data

    def set_instance_values(self, instance):
        for field in self.fields.keys():
            value = self.cleaned_data.get(field)
            setattr(instance, field, value)         

    def set_initial_values(self, instance):
        for field in self.fields.keys():
            self.fields[field].initial = getattr(instance, field)

    def get_changed_fields(self, model_object):
        changed = {}
        for field in self.fields.keys():
            if self.cleaned_data.get(field) != getattr(model_object, field):
                changed[field] = True

        return changed

class CFDFormset(forms.BaseFormSet):

    def save(self, parent_pk, current_user):

        record = m.cfd.objects.get(pk=parent_pk)
        formset_length = len(self)

        records = [record]
        records.extend(record.get_subsequent_contracts(formset_length - 1))
    
        for index, item in enumerate(self.forms):        
            if item.is_valid():
                current_record = records[index]

                item.set_instance_values(current_record)
                with reversion.create_revision():
                    
                    reversion.set_user(current_user)

                    changed_fields = current_record.get_changed_fields()
                    comments = ""
                    for field in changed_fields.keys():
                        old_value, new_value = changed_fields[field]
                        comments += f"Changed {m.cfd._meta.get_field(field).verbose_name} from {old_value} to {new_value};\n"

                    reversion.set_comment(comments)

                    current_record.save()   
                

    def get_changed_fields(self, parent_pk, records=None):
    
        record = m.cfd.objects.get(pk=parent_pk)
        formset_length = len(self.forms)

        records = [record]
        records.extend(record.get_subsequent_contracts(formset_length - 1))
        
        changed = []
        if self.is_valid():
            for index, item in enumerate(records):
                changed.append(self.forms[index].get_changed_fields(item))
        
        return changed
        
        

class CFDSearchForm(forms.Form):
    client_name = forms.CharField(label='', max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder' : 'Client Name'
        })
    )
    start_date = forms.DateField(required=False,
        widget=forms.TextInput(attrs={
                'placeholder' : 'Start Date'
            })
    )
    end_date = forms.DateField(required=False,
        widget=forms.TextInput(attrs={
            'placeholder' : 'End Date'
        })
    )