from django.core.files.base import ContentFile
from django.http import *
from django.shortcuts import *
from LSEGapp.forms import *
from LSEGapp.models import *
from django.forms.formsets import *
from django.db import IntegrityError
from django.forms.utils import ErrorList
from django.core.files import *
import json
import os
import zipfile
import io
from datetime import  datetime
import yaml

# MAIN PAGES VIEWS
def index(request):
    environment = Environment.objects.first()
    if request.method == 'POST':  # If the form has been submitted...
        form = EnvironmentForm(request.POST)  # A form bound to the POST data
        if form.is_valid():
            environment = form.cleaned_data['environment']
    else:
        form = EnvironmentForm()

    return render(request, 'index.html', locals())



def get_hosts(request):
    if request.is_ajax:
        #TAKE DATA FROM AJAX CALL
        host_filter = request.POST['host_filter']
        id_env = request.POST['id_env']
        environment = Environment.objects.get(id=id_env)
        hosts_roles = HostRole.objects.filter(host__environment=environment).order_by('host__name')
        #FILTERING
        if host_filter != "":
            hosts = Host.objects.all().filter(name__contains=host_filter)
            hosts_roles = hosts_roles.filter(host=hosts)

        dict ={}
        hosts_roles_list = []

        if hosts_roles.exists():
            host_role_old = hosts_roles[0]
            host_role = hosts_roles[0]
            role_text = '<a href= " role_details/' + str(host_role_old.host.id) + '/' + str(host_role_old.role.id) + '">'  + host_role_old.role.name + '</a>'

            for host_role in hosts_roles[1:]:
                if host_role.host.name == host_role_old.host.name:
                    role_text = role_text + '<br><a href= " role_details/' + str(host_role.host.id) + '/' + str(host_role.role.id) + '">' + host_role.role.name + '</a>'
                else:
                    host_text = '<a href= " host_details/' + str(host_role_old.host.id) + '">'  + host_role_old.host.name + '</a>'
                    record = {'id': host_role_old.host.id, 'host':host_text,'role_text': role_text}
                    hosts_roles_list.append(record)
                    role_text= '<a href= " role_details/' + str(host_role.host.id) + '/' + str(host_role.role.id) + '">' + host_role.role.name + '</a>'
                host_role_old = host_role

            if host_role.host.name == host_role_old.host.name:
                role_text = role_text
                host_text = '<a href= " host_details/' + str(host_role_old.host.id) + '">'  + host_role_old.host.name + '</a>'
                record = {'id': host_role_old.host.id, 'host':host_text,'role_text': role_text}
                hosts_roles_list.append(record)

        dict['host_roles'] = hosts_roles_list
        return JsonResponse(dict)
    else:
        return HttpResponse("You failled")

# ADD VIEWS
def add_host(request, id_env):
    environment = Environment.objects.get(id=id_env)

    RoleFormset = formset_factory(AddRoleForm)

    if request.method == 'POST':
        form2 = HostForm(request.POST)
        formset = RoleFormset(request.POST)

        if form2.is_valid():
            try:
                name = form2.cleaned_data['name']  # Get name from the form
                business_application = form2.cleaned_data['business_application']
                host = Host(name=name, environment=environment)
                host.save()  # Add a host

                roles_id = []

                for form in formset:
                    if form.is_valid():
                        role_name = form.cleaned_data['role']
                        role = Role.objects.get(name=role_name)
                        id = [role.id]
                        roles_id = roles_id + id

                save_roles(host, roles_id)
                return redirect(index)

            except IntegrityError:
                errors = form2._errors.setdefault("name", ErrorList())
                errors.append(u"This host already exists")

    else:
        ba_ids = RoleBusinessApplication.objects.all().values_list('business_application',flat=True).distinct() #LIST OF BusinessApplications ids when ba is used
        form2 = HostForm()
        form2.fields['business_application'].queryset = BusinessApplication.objects.all().filter(id__in= ba_ids)
        formset = RoleFormset()

    return render(request, 'normal_user/add_host.html', locals())

# EDIT VIEWS
def edit_host(request, id_host):
    host = Host.objects.get(id=id_host)
    environment = host.environment
    host_roles = HostRole.objects.filter(host=host)
    list_of_roles = host_roles.values('role')
    role = Role.objects.get(id=list_of_roles[0]['role'])
    business_application = RoleBusinessApplication.objects.filter(role=role).first().business_application
    RoleFormset = formset_factory(AddRoleForm,extra=0)
    if request.method == 'POST':
        form2 = EnvironmentForm(request.POST)
        form3 = HostForm(request.POST)
        formset = RoleFormset(request.POST)
        host_roles.delete()
        if form2.is_valid():
            environment = form2.cleaned_data['environment']
            host.environment = environment
        if formset.is_valid():
            roles_id = []
            for form in formset:
                role = form.cleaned_data['role']
                id = [role.id]
                roles_id = roles_id + id
            save_roles(host, roles_id)
        try:
            if form3.is_valid():
                name = form3.cleaned_data['name']
                host.name = name
                host.save()
            business_application = form3.cleaned_data['business_application']

            return redirect(host_details, id_host=id_host)

        except IntegrityError:
            errors = form3._errors.setdefault("name", ErrorList())
            errors.append(u"This host already exists")

    else:
        ba_ids = RoleBusinessApplication.objects.all().values_list('business_application',flat=True).distinct() #LIST OF BusinessApplications ids when ba is used
        form2 = EnvironmentForm()
        form2['environment'].initial = {'environment': environment}
        form3 = HostForm(initial={'name': host.name, 'business_application': business_application})
        form3.fields['business_application'].queryset = BusinessApplication.objects.all().filter(id__in= ba_ids)
        formset = RoleFormset(initial=list_of_roles)

    return render(request, 'normal_user/edit_host.html', locals())



def save_roles(host, roles_id):
    for role_id in roles_id:
        host_role = HostRole(host=host, role=Role.objects.get(id=role_id))
        host_role.save()  # Add a host role
        role_components_template = RoleComponentsTemplate.objects.filter(role=Role.objects.get(id=role_id))

        for role_component_template in role_components_template:  #THIS LOOP ADDS THE DIFFERENT COMPONENTS OF A TEMPLATE ROLE
            component = role_component_template.component
            role_component = RoleComponents(host_role=host_role, component=component)
            role_component.save()  # Save the role_component generated from the template
            component_variables_template = ComponentVariablesTemplate.objects.filter(
                component=Component.objects.get(name=component.name))

            for component_variable_template in component_variables_template:  # THIS LOOP ADDS THE DIFFERENT VARIABLES OF A COMPONENT TEMPLATE
                variable = component_variable_template.variable
                component_variable = ComponentVariables(role_component=role_component, variable=variable)
                component_variable.save()



def edit_value(request):
    if request.is_ajax:
        new_value = request.POST['new_value']
        component_var_id = request.POST['component_var_id']
        component_variable = ComponentVariables.objects.get(id=component_var_id)
        component_variable.value = new_value
        component_variable.save()
        return HttpResponse(" Successful edited value")
    else:
        return HttpResponse("FAIL")


# DELETE METHODS/VIEWS
def delete_host(request):
    if request.is_ajax:
        host_id = request.POST['host_id']
        host = Host.objects.get(id=host_id)
        HostRole.objects.filter(host=host).delete()
        host.delete()
        return HttpResponse('Success')
    else:
        return HttpResponse('You Failed')


# DETAILS VIEWS


def host_details(request, id_host):
    host = Host.objects.get(id=id_host)
    host_roles = HostRole.objects.filter(host=host)
    roles_components = RoleComponents.objects.filter(host_role=host_roles)
    object_list = []

    role_component_old = roles_components[0]
    variable_list = ComponentVariables.objects.filter(role_component=role_component_old)
    object = [ComponentVariableList(role_component=role_component_old, variable_list=variable_list)]
    object_list = object_list + object

    for role_component in roles_components[1:]:
        variable_list = ComponentVariables.objects.filter(role_component=role_component)
        if role_component.host_role.role == role_component_old.host_role.role:
            role_component_old = role_component
            role_component.host_role.role.name = ""
        else:
            role_component_old = role_component
        object = [ComponentVariableList(role_component=role_component, variable_list=variable_list)]
        object_list = object_list + object

    return render(request, 'normal_user/host_details.html', locals())


def role_details(request, id_host, id_role):
    host = Host.objects.get(id=id_host)
    role = Role.objects.get(id=id_role)
    host_role = HostRole.objects.get(host=host, role=role)
    role_components = RoleComponents.objects.filter(host_role=host_role)
    components_variables = ComponentVariables.objects.filter(role_component=role_components)

    return render(request, 'normal_user/role_details.html', locals())


# CUSTOM VIEWS

def set_default(request):
    if request.is_ajax:
        component_var_id = request.POST['component_var_id']
        component_variable = ComponentVariables.objects.get(id=component_var_id)
        component_variable.value = ""
        component_variable.save()
        value = component_variable.variable.default_value
        data = {'old_value': value}
        return JsonResponse(data)
    else:
        return HttpResponse("Ramy you failed")


def autocomplete_role_name(request):
    if request.is_ajax:
        business_app = request.POST['business_app']
        ba = BusinessApplication.objects.get(name=business_app)
        prefix = ba.prefix
        data = {'prefix': prefix}
        return JsonResponse(data)
    else:
        return HttpResponse("Ramy you failed")


def save_files(request):
    if request.is_ajax():
        hosts_ids = json.loads(request.POST['myarray'])

        hosts = Host.objects.filter(id__in=hosts_ids)

        for host in hosts:

            host_roles = HostRole.objects.all().filter(host=host)
            roles_components = RoleComponents.objects.all().filter(host_role=host_roles)
            components_variables = ComponentVariables.objects.all().filter(role_component=roles_components)

            with open('tmp/' + host.name +'.yaml', 'w') as f:
                myfile = File(f)
                list = [components_variables[0]]

                for component_variable in components_variables[1:]:  #We only save the variable that are not in the list already.
                    i = 0
                    found = False
                    while i < len(list) and (not found):
                        found = component_variable.variable.name == list[i].variable.name
                        i= i+1

                    if (not found):
                        list = list + [component_variable]

                for component_variable in list:
                    variable = component_variable.variable.name
                    myfile.write(variable + ": ")
                    if component_variable.value == "":
                        myfile.write("\'" + component_variable.variable.default_value + "\' \n")
                    else:
                        myfile.write("\'" + component_variable.value + "\' \n")

        return HttpResponse('Success')

def save_zip(request,id_env):
    environment = Environment.objects.get(id=id_env)
    date = datetime.now()

    # Files (local path) to put in the .zip
    filenames = os.listdir("tmp")
    root = "tmp/"
    files_list = []

    for file in filenames:
        files_list = files_list + [os.path.join(root,file)]

    # Folder name in ZIP archive which contains the above files
    zip_subdir = "YAML_" + environment.name + "_" + str(date.day) + '_' + str(date.month) + '_' + str(date.year) + '_' + str(date.hour) + '-' + str(date.minute)
    zip_filename = "%s.zip" % zip_subdir

    # Open StringIO to grab in-memory ZIP contents
    s = io.BytesIO()

    # The zip compressor
    zf = zipfile.ZipFile(s, "w")

    for fpath in files_list:
        # Calculate path for file in zip
        fdir, fname = os.path.split(fpath)
        zip_path = os.path.join(zip_subdir, fname)

        # Add file, at correct path
        zf.write(fpath, zip_path)

    # Must close zip for all contents to be written
    zf.close()

    #Delete the file stored in tmp
    for the_file in os.listdir(root):
        file_path = os.path.join(root, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception:
            print('Exceptions!')


    # Grab ZIP file from in-memory, make response with correct MIME-type
    resp = HttpResponse(s.getvalue())
    # ..and correct content-disposition
    resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

    return resp


def save_file(request,id_host):
    host = Host.objects.get(id=id_host)
    host_roles = HostRole.objects.all().filter(host=host)
    roles_components = RoleComponents.objects.all().filter(host_role=host_roles)
    components_variables = ComponentVariables.objects.all().filter(role_component=roles_components)
    response = HttpResponse(content_type='text/txt')

    response['Content-Disposition'] = "attachment; filename=" + host.name + ".yaml"

    list = [components_variables[0]]

    for component_variable in components_variables[1:]:  #We only save the variable that are not in the list already.
        i = 0
        found = False
        while i < len(list) and (not found):
            found = component_variable.variable.name == list[i].variable.name
            i= i+1

        if (not found):
            list = list + [component_variable]


    for component_variable in list:
        variable = component_variable.variable.name
        response.write(variable + ": ")
        if component_variable.value == "":
            response.write("\'" + component_variable.variable.default_value + "\' \n")
        else:
            response.write(component_variable.value + "\n")

    return response






