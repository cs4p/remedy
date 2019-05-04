from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory

from cfd.models import cfd
import cfd.forms as f

RETAIL_90_MAIL_RATES_B_LIST = ["GUAR_BR90_EZBD_DCT", "GUAR_BR90_IZBD_DCT", "GUAR_BR90_DISP_FEE",
                                   "RETAIL_90_MAIL_RATES_B_DS"]
RETAIL_90_MAIL_RATES_G_LIST = ["THEN GUAR_GR90_EZBD_DCT", "GUAR_GR90_IZBD_DCT", "GUAR_GR90_DISP_FEE",
                                   "RETAIL_90_MAIL_RATES_G_DS"]

@login_required
def cfd_list(request, template_name='cfd_list.html'):
    records = cfd.objects.filter(IS_TEMPLATE=False)
    data = {}
    data['object_list'] = records
    return render(request, template_name, data)

@login_required
def template_list(request, template_name='template_list.html'):
    records = cfd.objects.filter(IS_TEMPLATE=True)
    data = {}
    data['object_list'] = records
    return render(request, template_name, data)

@login_required
def cfd_create(request, template_name='cfd_form.html'):
    form = f.CFDForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('cfd:cfd_list')
    return render(request, template_name, {'form': form, "RETAIL_90_MAIL_RATES_B_LIST": RETAIL_90_MAIL_RATES_B_LIST, "RETAIL_90_MAIL_RATES_G_LIST":RETAIL_90_MAIL_RATES_G_LIST})

@login_required
def cfd_update(request, pk, template_name='cfd_form.html'):
    record = get_object_or_404(cfd, pk=pk)
    form = f.CFDForm(request.POST or None, instance=record)
    if form.is_valid():
        form.save()
        return redirect('cfd:cfd_list')
    return render(request, template_name, {'form': form, "RETAIL_90_MAIL_RATES_B_LIST": RETAIL_90_MAIL_RATES_B_LIST, "RETAIL_90_MAIL_RATES_G_LIST":RETAIL_90_MAIL_RATES_G_LIST})

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
        form.save()
        return redirect('cfd:cfd_list')
    return render(request, template_name, {'form': form, "RETAIL_90_MAIL_RATES_B_LIST": RETAIL_90_MAIL_RATES_B_LIST,
                                           "RETAIL_90_MAIL_RATES_G_LIST": RETAIL_90_MAIL_RATES_G_LIST})

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
    return render(request, template_name, {'formset': CFDFormSet, 'form': form, "RETAIL_90_MAIL_RATES_B_LIST": RETAIL_90_MAIL_RATES_B_LIST,
                                           "RETAIL_90_MAIL_RATES_G_LIST": RETAIL_90_MAIL_RATES_G_LIST})

