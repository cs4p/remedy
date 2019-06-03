from django.forms import formset_factory
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect, get_object_or_404

import reversion

import cfd.forms as f
from cfd.models import cfd
from cfd.admin import cfdAdmin

RETAIL_90_MAIL_RATES_B_LIST = ["GUAR_BR90_EZBD_DCT", "GUAR_BR90_IZBD_DCT", "GUAR_BR90_DISP_FEE",
                                   "RETAIL_90_MAIL_RATES_B_DS"]
RETAIL_90_MAIL_RATES_G_LIST = ["THEN GUAR_GR90_EZBD_DCT", "GUAR_GR90_IZBD_DCT", "GUAR_GR90_DISP_FEE",
                                   "RETAIL_90_MAIL_RATES_G_DS"]

@login_required
def cfd_list(request, template_name='cfd_list.html'):
    if request.method == "POST":
        form = f.CFDSearchForm(request.POST)

        if form.is_valid():
            records = cfd.search(**form.cleaned_data)
            client_data = records.filter(IS_TEMPLATE=False, confirmed=True)
            templates = records.filter(IS_TEMPLATE=True)
            pending = records.filter(confirmed=False)

            context = {
                'form' : form,
                'object_list' : client_data,
                'templates' : templates,
                'pending' : pending
            }

            return render(request, template_name, context)

    form = f.CFDSearchForm()
    records = cfd.objects.filter(IS_TEMPLATE=False, confirmed=True)
    templates = cfd.objects.filter(IS_TEMPLATE=True)
    pending = cfd.objects.filter(confirmed=False)

    context = {
        'form' : form,
        'object_list' : records,
        'templates' : templates,
        'pending' : pending
    }
      
    return render(request, template_name, context)

@login_required
@require_http_methods(["GET"])
def template_list(request, template_name='template_list.html'):
    records = cfd.objects.filter(IS_TEMPLATE=True)
    data = {
        'object_list' : records
    }
    return render(request, template_name, data)

@login_required
def cfd_create(request, template_name='cfd_form.html'):
    CFDFormset = formset_factory(f.CFDForm, extra=3)

    context = {        
        'formset' : None,
        'fieldsets' : f.CFDForm.Meta.fieldsets,
        'RETAIL_90_MAIL_RATES_B_LIST': RETAIL_90_MAIL_RATES_B_LIST,
        'RETAIL_90_MAIL_RATES_G_LIST': RETAIL_90_MAIL_RATES_G_LIST,
        'create' : True
    }    

    if request.method == "POST":        
        formset = CFDFormset(request.POST)
        
        if formset.is_valid():
            with reversion.create_revision():                    
                reversion.set_user(request.user)
                reversion.set_comment("Created")
                for form in formset:
                    form.save()

            return redirect('cfd:cfd_list')
        else:
            context['formset'] = formset

            return render(request, template_name, context)

    formset = CFDFormset()    
    context['formset'] = formset   

    return render(request, template_name, context)

@login_required
def cfd_update(request, pk, template_name='cfd_form.html'):
    record = get_object_or_404(cfd, pk=pk)
    CFDFormset = formset_factory(f.CFDForm, extra=3)
    
    if request.method == "POST":        
        formset = CFDFormset(request.POST)        

        confirmed = request.POST.get('is_confirmation_page', False)
        confirmed = confirmed == "True"

        if formset.is_valid():            
            return cfd_confirmation(request, pk, formset, confirmed)
        else:
            context = {    
                'formset' : formset,
                'fieldsets' : f.CFDForm.Meta.fieldsets,
                'RETAIL_90_MAIL_RATES_B_LIST': RETAIL_90_MAIL_RATES_B_LIST,
                'RETAIL_90_MAIL_RATES_G_LIST': RETAIL_90_MAIL_RATES_G_LIST
            }

            return render(request, template_name, context)

    record1, record2 = record.get_subsequent_contracts(2)

    formset = CFDFormset()
    formset[0].set_initial_values(record)
    formset[1].set_initial_values(record1)
    formset[2].set_initial_values(record2)

    context = {    
        'formset' : formset,
        'fieldsets' : f.CFDForm.Meta.fieldsets,
        'RETAIL_90_MAIL_RATES_B_LIST': RETAIL_90_MAIL_RATES_B_LIST,
        'RETAIL_90_MAIL_RATES_G_LIST': RETAIL_90_MAIL_RATES_G_LIST
    }
    
    return render(request, template_name, context)

@login_required
def cfd_confirmation(request, pk, formset, confirmed, template_name='cfd_confirmation.html'):
    CFDFormset = formset_factory(f.CFDForm, formset=f.CFDFormset, extra=3)

    if request.method == "POST":    
        formset = CFDFormset(request.POST)
        if confirmed:                     
            if formset.is_valid():
                formset.save(pk, request.user)

                return redirect('cfd:cfd_list')
            else:
                context = {    
                    'formset' : formset,
                    'fieldsets' : f.CFDForm.Meta.fieldsets,
                    'RETAIL_90_MAIL_RATES_B_LIST': RETAIL_90_MAIL_RATES_B_LIST,
                    'RETAIL_90_MAIL_RATES_G_LIST': RETAIL_90_MAIL_RATES_G_LIST
                }

                return render(request, "cfd_form.html", context)
        else:
            context = {    
                'formset' : formset,
                'fieldsets' : f.CFDForm.Meta.fieldsets,
                'confirmation' : True,
                'changed' : formset.get_changed_fields(parent_pk=pk)
            }

            return render(request, template_name, context)


@login_required
def cfd_delete(request, pk, template_name='cfd_delete.html'):
    record = get_object_or_404(cfd, pk=pk)
    if request.method=='POST':
        record.delete()
        return redirect('cfd:cfd_list')
    return render(request, template_name, {'object': record})

@login_required
def cfd_copy(request, pk, template_name="cfd_form.html"):
    record = get_object_or_404(cfd, pk=pk)
    record.pk=None
    form = f.CFDForm(request.POST or None, instance=record)
    if form.is_valid():
        with reversion.create_revision():                    
            reversion.set_user(request.user)
            reversion.set_comment("Created")
            form.save()
            return redirect('cfd:cfd_list')
    
    context = {
        'form': form, 
        'fieldsets' : form.Meta.fieldsets,
        'RETAIL_90_MAIL_RATES_B_LIST': RETAIL_90_MAIL_RATES_B_LIST,
        'RETAIL_90_MAIL_RATES_G_LIST': RETAIL_90_MAIL_RATES_G_LIST
        }

    return render(request, template_name, context)

@login_required
def cfd_create_mutiple(request, template_name="cfd_new_multi.html"):
    # Create the formset, specifying the form and formset we want to use.
    CFDFormSet = formset_factory(f.CFDForm,extra=3)
    # and a blank form for the row headers
    form = f.CFDForm()
    if request.method == 'POST':
        response = CFDFormSet(request.POST)
        if response.is_valid():
            response.save()
        return redirect('cfd:cfd_list')
    return render(request, template_name, {'formset': CFDFormSet, 'form': form, 'RETAIL_90_MAIL_RATES_B_LIST': RETAIL_90_MAIL_RATES_B_LIST,
                                           'RETAIL_90_MAIL_RATES_G_LIST': RETAIL_90_MAIL_RATES_G_LIST})


@login_required
@require_http_methods(["GET"])
def cfd_history(request, pk):
    record = get_object_or_404(cfd, pk=pk)
    
    logs = cfd.history.all_record_logs(record)

    context = {
        'record' : record,
        'logs' : logs
    }
    
    return render(request, 'cfd_history.html', context)

@login_required
def cfd_history_detail(request, pk, detail_pk):
    record = get_object_or_404(cfd, pk=pk)
    
    version = cfd.history.filter_record_logs(record, pk=detail_pk).get()
    version = version._object_version.object

    form = f.CFDForm(request.POST or None, instance=version)

    if form.is_valid():
        with reversion.create_revision():                    
            reversion.set_user(request.user)
            reversion.set_comment("Reverted to previous version")
            form.save()

        return redirect('cfd:cfd_list')

    context = {
        'record' : record,
        'version' : version,
        'form' : form,
        'fieldsets' : form.Meta.fieldsets
    }
    
    return render(request, 'cfd_recover_form.html', context)