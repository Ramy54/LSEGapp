__author__ = 'ramyah'

from django.http import *
from django.shortcuts import *
from LSEGapp.forms import *
from LSEGapp.models import *
from django.forms.formsets import *
from django.db import IntegrityError
from django.forms.utils import ErrorList
from LSEGapp.views import views


def component_template(request):
    components_variables = ComponentVariablesTemplate.objects.all()
    return render(request, 'template/component_template.html', locals())



def get_components(request):
    if request.is_ajax:
        component_filter = request.POST['component_filter']
        components_variables = ComponentVariablesTemplate.objects.all().order_by('component__name')
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
                    record = {'id': component_variable_old.component.id, 'component':component_variable_old.component.name,'variable_text': variable_text}
                    components_variables_list.append(record)
                    variable_text= '<a>' + component_variable.variable.name + '</a>'
                component_variable_old = component_variable

            if component_variable.component.name == component_variable_old.component.name:
                variable_text = variable_text
                record = {'id': component_variable_old.component.id, 'component': component_variable_old.component.name,'variable_text': variable_text}
                components_variables_list.append(record)

        dict['components_vars'] = components_variables_list
        return JsonResponse(dict)
    else:
        return HttpResponse("You failled")


def add_component_template(request):
    VariableFormset = formsets.formset_factory(AddVariableForm, can_delete=True)

    if request.method == 'POST':
        form2 = ComponentForm(request.POST)
        formset = VariableFormset(request.POST)
        if form2.is_valid():
            try:
                name = form2.cleaned_data['name']  # Get name from the form
                component = Component(name=name)
                component.save()
                if formset.is_valid():
                    for form in formset:
                        var = form.cleaned_data['variable']
                        component_variable = ComponentVariablesTemplate(component=component, variable=var)
                        component_variable.save()
                    return redirect(component_template)

            except IntegrityError:
                errors = form2._errors.setdefault("name", ErrorList())
                errors.append(u"This component already exists")

    else:
        formset = VariableFormset()
        form2 = ComponentForm()

    return render(request, 'template/add_component_template.html', locals())


def edit_component_template(request, id_component):
    VariableFormset = formsets.formset_factory(AddVariableForm, extra=0)
    component = Component.objects.get(id=id_component)
    list_of_variables = ComponentVariablesTemplate.objects.filter(component=component).values('variable')

    if request.method == 'POST':
        form2 = ComponentForm(request.POST)
        formset = VariableFormset(request.POST)
        if form2.is_valid():
            try:
                name = form2.cleaned_data['name']
                component.name = name
                component.save()
                ComponentVariablesTemplate.objects.filter(component=component).delete()
                if formset.is_valid():
                    for form in formset:
                        if form.is_valid():
                            variable = form.cleaned_data['variable']
                            component_variable = ComponentVariablesTemplate(component=component, variable=variable)
                            component_variable.save()

                return redirect(component_template)
            except IntegrityError:
                errors = form2._errors.setdefault("name", ErrorList())
                errors.append(u"This component already exists")

    else:
        formset = VariableFormset(initial=list_of_variables)
        form2 = ComponentForm(initial={'name': component.name})

    return render(request, 'template/edit_component_template.html', locals())


def delete_component_template(request):
    if request.is_ajax:
        component_name = request.POST['component_name']
        component = Component.objects.get(name=component_name)
        component.delete()
        return HttpResponse('Success')

    else:
        return HttpResponse('You Failed')


def is_component_used(request):
    if request.is_ajax:
        component_name = request.POST['component_name']
        component = Component.objects.get(name=component_name)
        role_comps = RoleComponentsTemplate.objects.filter(component=component)
        if not(role_comps.exists()):
            used = False
            return JsonResponse({'boolean': used})

        else:
            used = True
            message = "The component " + component.name + " is used"
            return JsonResponse({'boolean': used, 'message':message})
    else:
        return HttpResponse('You Failled')