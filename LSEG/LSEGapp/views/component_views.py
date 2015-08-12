__author__ = 'ramyah'

from django.http import *
from django.shortcuts import *
from LSEGapp.forms import *
from LSEGapp.models import *
from django.forms.formsets import *
from django.db import IntegrityError
from django.forms.utils import ErrorList

def get_components(request):
    if request.is_ajax:
        component_filter = request.POST['component_filter']
        components_variables = ComponentVariablesTemplate.objects.all()
        if component_filter != "":
            components = Component.objects.all().filter(name__contains=component_filter)
            components_variables = components_variables.filter(component=components)

        dict ={}
        components_variables_list = []

        if components_variables.exists():
            component_variable = components_variables[0]
            component_variable_old = components_variables[0]
            variable_text = '<a>' + component_variable_old.variable.name + '</a>'

            for component_variable in components_variables[1:]:
                if component_variable.component.name == component_variable_old.component.name:
                    variable_text = variable_text + '<br><a>' + component_variable.variable.name + '</a>'
                else:
                    record = {'id': component_variable.id, 'component':component_variable_old.component.name,'variable_text': variable_text}
                    components_variables_list.append(record)
                    variable_text= '<a>' + component_variable.variable.name + '</a>'
                component_variable_old = component_variable

            if component_variable.component.name == component_variable_old.component.name:
                variable_text = variable_text
                record = {'id': component_variable.id, 'component': component_variable_old.component.name,'variable_text': variable_text}
                components_variables_list.append(record)

        dict['components_vars'] = components_variables_list
        return JsonResponse(dict)
    else:
        return HttpResponse("You failled")


def delete_component(request):
    if request.is_ajax:
        component_name = request.POST['component_name']
        component = Component.objects.get(name=component_name)
        component.delete()
        return HttpResponse('Success')

    else:
        return HttpResponse('You Failed')
