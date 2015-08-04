from django.contrib import admin
from LSEGapp.models import *


class EnvironmentAdmin(admin.ModelAdmin):
    list_display = ('name',)

class BusinessApplicationAdmin(admin.ModelAdmin):
    list_display = ('name',)

class HostAdmin(admin.ModelAdmin):
    list_display = ('name', 'environment')
    list_filter = ('environment',)
    ordering = ('environment', 'name')

class HostBusinessApplicationAdmin(admin.ModelAdmin):
    list_display = ('host', 'business_application')
    list_filter = ('business_application',)
    ordering = ('business_application', 'host')

class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)

class ComponentAdmin(admin.ModelAdmin):
    list_display = ('name',)

class VariableAdmin(admin.ModelAdmin):
    list_display = ('name', 'default_value', 'type', 'required', 'description')
    list_filter = ('type', 'required')
    ordering = ('name',)

class HostRoleAdmin(admin.ModelAdmin):
    list_display = ('host', 'role')
    list_filter = ('host', 'role')
    ordering = ('host',)

class RoleComponentsTemplateAdmin(admin.ModelAdmin):
    list_display = ('role', 'component')
    list_filter = ('role', 'component')
    ordering = ('role', 'component')

class ComponentVariablesTemplateAdmin(admin.ModelAdmin):
    list_display = ('component', 'variable')
    list_filter = ('component', 'variable')
    ordering = ('component', 'variable')

class RoleComponentsAdmin(admin.ModelAdmin):
    list_display = ('host_role', 'component')
    list_filter = ('host_role', 'component')
    ordering = ('host_role', 'component')

class ComponentVariablesAdmin(admin.ModelAdmin):
    list_display = ('role_component', 'variable','value')
    list_filter = ('role_component', 'variable','value')
    ordering = ('role_component', 'variable')


# Register your models here.

admin.site.register(Environment, EnvironmentAdmin)
admin.site.register(BusinessApplication,BusinessApplicationAdmin)
admin.site.register(Host,HostAdmin)
admin.site.register(HostBusinessApplication,HostBusinessApplicationAdmin)
admin.site.register(Role,RoleAdmin)
admin.site.register(Component,ComponentAdmin)
admin.site.register(Variable,VariableAdmin)
admin.site.register(HostRole,HostRoleAdmin)
admin.site.register(RoleComponentsTemplate,RoleComponentsTemplateAdmin)
admin.site.register(ComponentVariablesTemplate,ComponentVariablesTemplateAdmin)
admin.site.register(RoleComponents,RoleComponentsAdmin)
admin.site.register(ComponentVariables,ComponentVariablesAdmin)