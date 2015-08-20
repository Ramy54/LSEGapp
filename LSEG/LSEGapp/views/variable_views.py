__author__ = 'ramyah'

from django.http import *
from django.shortcuts import *
from LSEGapp.forms import *
from LSEGapp.models import *
from django.forms.formsets import *
from django.db import IntegrityError
from django.forms.utils import ErrorList
import os
import yaml
from LSEGapp.views.views import *


def variables(request):
    if request.method == 'POST':

        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
    else:
        form = UploadFileForm()

    return render(request, 'template/variables/variables.html', locals())


def handle_uploaded_file(f):
    with open('tmp/' + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    read_file()



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


def read_file():
    # INITIALIZATION
    filenames = os.listdir("tmp") ## all files in tmp
    root = "tmp/"
    files_list = []

    for file in filenames:
        files_list = files_list + [os.path.join(root,file)]

    #TAKE FILE ONE BY ONE AND SAVE VARIABLE TO DATABASE

    for file in files_list:
        with open(file, 'r') as stream:
            content= yaml.load(stream)     #Content of the YAML as a dictonary {key : value}

        for key, value in content.items():
            var_name = key
            var_value = value
            try:
                var = Variable(name=var_name, default_value=var_value, type="String", required = True)
                var.save()
            except IntegrityError:
                continue

  #Delete the file stored in tmp
    for the_file in os.listdir(root):
        file_path = os.path.join(root, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception:
            print('Exceptions!')