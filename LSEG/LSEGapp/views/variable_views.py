__author__ = 'ramyah'

from django.http import *
from django.shortcuts import *
from LSEGapp.forms import *
from LSEGapp.models import *
from django.forms.formsets import *
from django.db import IntegrityError
from django.forms.utils import ErrorList


def variables(request, delete_message=0):
    if delete_message == '1':
        message = "Variable deleted."
    if delete_message == '2':
        message = "This variable is used. Please clear all dependencies."

    variables = Variable.objects.all()  # The variables to be given to the template

    if request.method == 'POST':
        form = VariableForm(request.POST)
        if form.is_valid():
            try:
                name = form.cleaned_data['name']
                default_value = form.cleaned_data['default_value']
                type = form.cleaned_data['type']
                required = form.cleaned_data['required']
                description = form.cleaned_data['description']

                new_var = Variable(name=name, default_value=default_value, type=type, required=required,
                                   description=description)
                new_var.save()
            except IntegrityError:
                errors = form._errors.setdefault("name", ErrorList())
                errors.append(u"This variable already exists")
    else:
        form = VariableForm()

    return render(request, 'template/variables.html', locals())

def get_vars(request):
    if request.is_ajax:
        name_filter = request.POST['name_filter']
        type_filter = request.POST['type_filter']
        variables = Variable.objects.all()
        if name_filter != "":
            variables = variables.filter(name__contains=name_filter)
        if type_filter != "":
            variables = variables.filter(type__contains=type_filter)

        dict = {}
        variable_list = []
        for variable in variables:
            record = {'id': variable.id, 'name': variable.name, 'type': variable.type, 'default_value': variable.default_value, 'required':variable.required, 'description': variable.description}
            variable_list.append(record)

        dict['variable'] = variable_list
        return JsonResponse(dict)
    else:
        return HttpResponse("You failled")


def add_variable(request):
    if request.is_ajax:
        name = request.POST['name']
        type = request.POST['type']
        default_value = request.POST['default_value']
        required = request.POST['required']
        if required == "false":
            required = False
        else:
            required = True
        description = request.POST['description']
        Variable(name=name,type=type,default_value=default_value,required=required,description=description).save()
        add_message = "The variable " + name + " has been added successfully "
        return HttpResponse('Success')
    else:
        return HttpResponse("Fail")

def delete_variable(request):
    if request.is_ajax:
        var_name = request.POST['var_name']
        var = Variable.objects.get(name=var_name)
        compo_vars = ComponentVariablesTemplate.objects.filter(variable=var)
        if not(compo_vars.exists()):
            message = 'The variable ' + var.name + ' has been deleted.'
            var.delete()
            boolean = True
            return JsonResponse({'message': message,'boolean': boolean})

        else:
            boolean=False
            message = "The variable" + var.name + "can't be deleted"
            return JsonResponse({'message':message, 'boolean': boolean})
    else:
        return HttpResponse('You Failled')


def update_variable(request):
    if request.is_ajax:
        id = request.POST['id']
        name = request.POST['name']
        type = request.POST['type']
        default_value = request.POST['default_value']
        required = request.POST['required']
        if required == "false":
            required = False
        else:
            required = True
        description = request.POST['description']

        variable = Variable.objects.get(id=id)
        variable.name = name
        variable.type = type
        variable.default_value = default_value
        variable.required = required
        variable.description = description
        variable.save()

        return JsonResponse({})
    else:
        return HttpResponse('Faillure')


def is_var_used(request):
    if request.is_ajax:
        name = request.POST['name']
        var = Variable.objects.get(name=name)
        compo_vars = ComponentVariablesTemplate.objects.filter(variable=var)
        if not(compo_vars.exists()):
            used = False
            return JsonResponse({'boolean': used})

        else:
            used = True
            message = "The variable " + var.name + " is used"
            return JsonResponse({'boolean': used, 'message':message})
    else:
        return HttpResponse('You Failled')


def is_var_valid(request):
    if request.is_ajax:
        id = request.POST['id']
        new_name = request.POST['new_name']
        new_type = request.POST['new_type']
        new_default_value = request.POST['new_default_value']

        var = Variable.objects.get(id=id)
        if (Variable.objects.filter(name=new_name).exists() and new_name != var.name) or new_type == "" or new_default_value== "":
            valid = False
            message = "The variable " + new_name + "  is not valid"
            return JsonResponse({'boolean': False, 'message': message})

        else:
            valid = True

            return JsonResponse({'boolean': True, 'message':''})
    else:
        return HttpResponse('You Failled')


def is_var_valid2(request):
    if request.is_ajax:
        new_name = request.POST['new_name']
        new_type = request.POST['new_type']
        new_default_value = request.POST['new_default_value']

        if Variable.objects.filter(name=new_name).exists() or new_type == "" or new_default_value == "":
            valid = False
            message = "The variable " + new_name + "  is not valid"
            return JsonResponse({'boolean': False, 'message': message})

        else:
            valid = True

            return JsonResponse({'boolean': True, 'message':''})
    else:
        return HttpResponse('You Failled')

