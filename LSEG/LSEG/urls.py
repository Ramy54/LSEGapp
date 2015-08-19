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


                       #HOST&ROLE DETAILS URLS
                       url(r'^host_details/(?P<id_host>\d+)$', 'host_details'),
                       url(r'^role_details/(?P<id_host>\d+)/(?P<id_role>\d+)$','role_details'),
                       url(r'^edit_host/(?P<id_host>\d+)$', 'edit_host'),
                       url(r'^edit_value$', 'edit_value'),
                       url(r'^set_default$', 'set_default'),


                       #HOST URLS
                       url(r'^add_host/(?P<id_env>\d+)$', 'add_host'),
                       url(r'^save_file/(?P<id_host>\d+)$','save_file'),  # Generate the YAML
                       url(r'^save_files$','save_files'),  # Save the files in tmp
                       url(r'^save_zip/(?P<id_env>\d+)$','save_zip'),  # Generate the zip from saved_files
                       url(r'^read_file$','read_file'),
                       url(r'^get_hosts$', 'get_hosts'),
                       url(r'^delete_host$', 'delete_host'),


                       #ROLE TEMPLATE URLS (ALL THE VIEWS HERE ARE DEFINED IN role_views)
                       url(r'^role_template$', 'role_template'),
                       url(r'^get_roles$', 'get_roles'),
                       url(r'^add_role_template$', 'add_role_template'),
                       url(r'^edit_role_template/(?P<id_role>\d+)$', 'edit_role_template'),
                       url(r'^delete_role_template$', 'delete_role_template'),
                       url(r'^is_role_used$', 'is_role_used'),
                       url(r'^autocomplete_role_name$', 'autocomplete_role_name'),
                       url(r'^role_filter$', 'role_filter'),


                       #COMPONENT TEMPLATE URLS (ALL THE VIEWS HERE ARE DEFINED IN component_views)
                       url(r'^component_template$', 'component_template'),
                       url(r'^get_components$', 'get_components'),
                       url(r'^add_component_template$', 'add_component_template'),
                       url(r'^edit_component_template/(?P<id_component>\d+)$', 'edit_component_template'),
                       url(r'^delete_component_template$', 'delete_component_template'),
                       url(r'^is_component_used$', 'is_component_used'),


                       #VARIABLE URLS (ALL THE VIEWS HERE ARE DEFINED IN variable_views)
                       url(r'^variables$', 'variables'),
                       url(r'^get_vars$', 'get_vars'),
                       url(r'^add_variable$', 'add_variable'),
                       url(r'^delete_variable$','delete_variable'),
                       url(r'^update_variable$', 'update_variable'),
                       url(r'^is_var_used$', 'is_var_used'),
                       url(r'^is_var_valid$', 'is_var_valid'),
                       url(r'^is_var_valid2$', 'is_var_valid2'),


                       )

