from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django import forms
import logging

from cfd.models import cfd

def index(request):
    return HttpResponse("Hello, world. You're at the CFD Management index.")

    
class PostsForm(ModelForm):
    class Meta:
        model = cfd
        fields = '__all__'
    
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
    form = PostsForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('cfd:post_list')
    return render(request, template_name, {'form': form})

@login_required
def post_update(request, pk, template_name='cfd/post_form.html'):
    post = get_object_or_404(cfd, pk=pk)
    logger.info("START_DATE is %s" % post.START_DATE)
    logger.info("END_DATE is %s" % post.END_DATE)
    form = PostsForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('cfd:post_list')
    return render(request, template_name, {'form': form})

@login_required
def post_delete(request, pk, template_name='cfd/post_delete.html'):
    post = get_object_or_404(cfd, pk=pk)
    if request.method=='POST':
        post.delete()
        return redirect('cfd:post_list')
    return render(request, template_name, {'object': post})