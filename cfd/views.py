from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django import forms
from django.forms.widgets import DateInput, SelectMultiple
import logging

from cfd.models import cfd

def index(request):
    return HttpResponse("Hello, world. You're at the CFD Management index.")

    
class PostsForm(ModelForm):
    class Meta:
        DROP_DOWN_MENU_41 = (
            ('Transplant','Transplant'),
            ('Hepatitis B','Hepatitis B'),
            ('CMV Agents','CMV Agents'),
            ('HIV','HIV'),
            ('Anticoagulants','Anticoagulants'),
            ('Hepatitis C','Hepatitis C'),
            ('PCSK9','PCSK9')
            )
        
        model = cfd
        fields = '__all__'
        error_css_class = 'error'
        required_css_class = 'required'
        widgets = {
            'START_DATE': DateInput(attrs={'class':'datepicker'}),
            'END_DATE': DateInput(attrs={'class':'datepicker'}),
            'NON_SPC_CLASSES': forms.SelectMultiple(choices=DROP_DOWN_MENU_41),
        }
        
        
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("START_DATE")
        end_date = cleaned_data.get("END_DATE")

        if start_date and end_date:
            # Only do something if both fields are valid so far.
            if start_date > end_date:
                raise forms.ValidationError(
                    "The Contract Start Date must be earlier than the Contract End Date."
                )

logger = logging.getLogger('django.server')

@login_required
def post_list(request, template_name='cfd/post_list.html'):
    posts = cfd.objects.all()
    data = {}
    data['object_list'] = posts
    return render(request, template_name, data)

@login_required
def post_create(request, template_name='cfd/post_form.html'):
    RETAIL_90_MAIL_RATES_B_LIST = ["GUAR_BR90_EZBD_DCT", "GUAR_BR90_IZBD_DCT", "GUAR_BR90_DISP_FEE",
                                   "RETAIL_90_MAIL_RATES_B_DS"]
    RETAIL_90_MAIL_RATES_G_LIST = ["THEN GUAR_GR90_EZBD_DCT", "GUAR_GR90_IZBD_DCT", "GUAR_GR90_DISP_FEE",
                                   "RETAIL_90_MAIL_RATES_G_DS"]
    form = PostsForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('cfd:post_list')
    return render(request, template_name, {'form': form, "RETAIL_90_MAIL_RATES_B_LIST": RETAIL_90_MAIL_RATES_B_LIST, "RETAIL_90_MAIL_RATES_G_LIST":RETAIL_90_MAIL_RATES_G_LIST})

@login_required
def post_update(request, pk, template_name='cfd/post_form.html'):
    post = get_object_or_404(cfd, pk=pk)
    RETAIL_90_MAIL_RATES_B_LIST = ["GUAR_BR90_EZBD_DCT", "GUAR_BR90_IZBD_DCT", "GUAR_BR90_DISP_FEE",
                                   "RETAIL_90_MAIL_RATES_B_DS"]
    RETAIL_90_MAIL_RATES_G_LIST = ["THEN GUAR_GR90_EZBD_DCT", "GUAR_GR90_IZBD_DCT", "GUAR_GR90_DISP_FEE",
                                   "RETAIL_90_MAIL_RATES_G_DS"]
    form = PostsForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('cfd:post_list')
    return render(request, template_name, {'form': form, "RETAIL_90_MAIL_RATES_B_LIST": RETAIL_90_MAIL_RATES_B_LIST, "RETAIL_90_MAIL_RATES_G_LIST":RETAIL_90_MAIL_RATES_G_LIST})

@login_required
def post_delete(request, pk, template_name='cfd/post_delete.html'):
    post = get_object_or_404(cfd, pk=pk)
    if request.method=='POST':
        post.delete()
        return redirect('cfd:post_list')
    return render(request, template_name, {'object': post})