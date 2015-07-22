"""LSEG URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url,patterns
from django.contrib import admin
from LSEGapp.forms import *
from LSEGapp import views
urlpatterns = patterns('LSEGapp.views',

                       # MAIN URLS
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$','index'),
                       url(r'^bootstrap','bootstrap'),
                       url(r'^index$','index'),
                       url(r'^skeleton$','skeleton'),


                       #TEMPLATE URLS
                       url(r'^role_template$', 'role_template'),
                       url(r'component_template$', 'component_template'),
                       url(r'variables$', 'variables'),


                       #DETAILS URLS
                       url(r'host_details/(?P<id_host>\d+)$','host_details'),
                       url(r'role_details/(?P<id_host>\d+)/(?P<id_role>\d+)$','role_details'),
                       url(r'component_details/(?P<id_host>\d+)/(?P<id_role>\d+)/(?P<id_component>\d+)$','component_details'),


                       #ADD URLS
                       url(r'^add_host/(?P<id_env>\d+)$', 'add_host'),


                       #EDIT URLS
                       url(r'^edit_host/(?P<id_host>\d+)$', 'edit_host'),
                       url(r'edit_variable/(?P<id_var>\d+)$','edit_variable'),
                       url(r'edit_component_template/(?P<id_component>\d+)$', 'edit_component_template'),
                       url(r'edit_role_template/(?P<id_role>\d+)$', 'edit_role_template'),
                       url(r'edit_component/(?P<id_host>\d+)/(?P<id_role>\d+)/(?P<id_component>\d+)$', 'edit_component'),
                       url(r'edit_role/(?P<id_host>\d+)/(?P<id_role>\d+)$', 'edit_role'),



                       #DELETE URLS
                       url(r'^delete_host/(?P<id_host>\d+)$','delete_host'),
                       url(r'^role_template_delete/(?P<id>\d+)$', 'delete_role_template'),
                       url(r'^component_template_delete/(?P<id>\d+)$', 'delete_component_template'),
                       url(r'^variables/(?P<id>\d+)$','delete_variable'),

                       url(r'^role_delete/(?P<id_host>\d+)/(?P<id_host_role>\d+)$', 'delete_role'),
                       url(r'^component_delete/(?P<id_host>\d+)/(?P<id_role>\d+)/(?P<id_component>\d+)$', 'delete_component'),






                       )

