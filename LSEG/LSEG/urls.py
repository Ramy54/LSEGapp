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

urlpatterns = patterns('LSEGapp.views',

                       # MAIN URLS
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$','index'),
                       url(r'^index$','index'),
                       url(r'^skeleton$','skeleton'),


                       #TEMPLATE URLS
                       url(r'^role_template$', 'role_template'),
                       url(r'^role_template/(?P<delete_message>[0-2])$', 'role_template'),
                       url(r'component_template$', 'component_template'),
                       url(r'component_template/(?P<delete_message>[0-2])$', 'component_template'),
                       url(r'variables$', 'variables'),
                       url(r'variables/(?P<delete_message>[0-2])$', 'variables'),


                       #DETAILS URLS
                       url(r'host_details/(?P<id_host>\d+)$','host_details'),
                       url(r'host_details_2/(?P<id_host>\d+)$','host_details_2'),
                       url(r'role_details/(?P<id_host>\d+)/(?P<id_role>\d+)$','role_details'),
                       url(r'component_details/(?P<id_host>\d+)/(?P<id_role>\d+)/(?P<id_component>\d+)$','component_details'),


                       #ADD URLS
                       url(r'^add_host/(?P<id_env>\d+)$', 'add_host'),
                       url(r'^add_variable$', 'add_variable'),


                       #EDIT URLS
                       url(r'^edit_host/(?P<id_host>\d+)$', 'edit_host'),
                       url(r'edit_variable/(?P<id_var>\d+)$','edit_variable'),
                       url(r'edit_component_template/(?P<id_component>\d+)$', 'edit_component_template'),
                       url(r'edit_role_template/(?P<id_role>\d+)$', 'edit_role_template'),
                       url(r'edit_component/(?P<id_host>\d+)/(?P<id_role>\d+)/(?P<id_component>\d+)$', 'edit_component'),
                       url(r'edit_role/(?P<id_host>\d+)/(?P<id_role>\d+)$', 'edit_role'),
                       url(r'edit_value$', 'edit_value'),
                       url(r'edit_default_value$', 'edit_default_value'),
                       url(r'update_variable$', 'update_variable'),



                       #DELETE URLS
                       url(r'^delete_host/(?P<id_host>\d+)$','delete_host'),
                       url(r'^role_template_delete/(?P<id>\d+)$', 'delete_role_template'),
                       url(r'^component_template_delete/(?P<id>\d+)$', 'delete_component_template'),
                       url(r'^delete_variable$','delete_variable'),
                       url(r'^role_delete/(?P<id_host>\d+)/(?P<id_host_role>\d+)$', 'delete_role'),
                       url(r'^component_delete/(?P<id_host>\d+)/(?P<id_role>\d+)/(?P<id_component>\d+)$', 'delete_component'),

                       #CUSTOM URLS
                       url(r'save_file/(?P<id_host>\d+)$','save_file'),
                       url(r'set_default$', 'set_default'),
                       url(r'autocompletion_role_name$', 'autocompletion_role_name'),
                       url(r'role_filter$', 'role_filter'),
                       url(r'get_vars$', 'get_vars'),
                       url(r'is_var_used$', 'is_var_used'),



                       )

