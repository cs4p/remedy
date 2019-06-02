"""
crudapp URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
"""
from django.conf.urls import url
from django.urls import path, include
from django.contrib import admin
from cfd import views

#added for form preview
from django import forms

from cfd.forms import CFDForm
from cfd.forms import CFDFormPreview

app_name = 'cfd'
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.cfd_list, name='cfd_list'),
    url(r'^list$', views.cfd_list, name='cfd_list'),
    url(r'^templates$', views.template_list, name='template_list'),
    url(r'^new$', views.cfd_create, name='cfd_new'),
    url(r'^new_multi$', views.cfd_create_mutiple, name='cfd_new_multi'),
    url(r'^edit/(?P<pk>\d+)$', views.cfd_update, name='cfd_edit'),
    url(r'^copy/(?P<pk>\d+)$', views.cfd_copy, name='cfd_copy'),
    url(r'^history/(?P<pk>\d+)$', views.cfd_history, name='cfd_history'),
    url(r'^history/(?P<pk>\d+)/(?P<detail_pk>\d+)$', views.cfd_history_detail, name='cfd_history_detail'),
    url(r'^delete/(?P<pk>\d+)$', views.cfd_delete, name='cfd_delete'),
    url(r'^post/$', CFDFormPreview(CFDForm)),
    path('accounts/', include('django.contrib.auth.urls')),

]
