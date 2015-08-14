from django.http import *
from django.shortcuts import *
from LSEGapp.forms import *
from LSEGapp.models import *
from django.forms.formsets import *
from django.db import IntegrityError
from django.forms.utils import ErrorList


# MAIN PAGES VIEWS

def index(request):
    environment = Environment.objects.first()
    if request.method == 'POST':  # If the form has been submitted...
        form = EnvironmentForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            environment = form.cleaned_data['environment']

    else:
        form = EnvironmentForm()

    hosts = Host.objects.filter(environment=environment)
    host_roles = []
    for host in hosts:
        host_roles = host_roles + list(HostRole.objects.filter(host=host))

    return render(request, 'index.html', locals())


def skeleton(request):
    return render(request, "skeleton.html")


# TEMPLATE VIEWS
def role_template(request, delete_message=0):
    if delete_message == "1":
        message = "The role has been deleted"
    if delete_message == "2":
        message = "The role is used you can't delete it"

    ComponentFormset = formset_factory(AddComponentForm)
    roles_components = RoleComponentsTemplate.objects.all()

    if request.method == 'POST':
        form2 = RoleForm(request.POST)
        formset = ComponentFormset(request.POST)

        if form2.is_valid():
            try:
                name = form2.cleaned_data['name']  # Get name from the form
                business_application = form2.cleaned_data['business_application']

                role = Role(name=name)
                role.save()

                role_ba = RoleBusinessApplication(role=role, business_application=business_application)
                role_ba.save()
                if formset.is_valid():
                    for form in formset:
                        component = form.cleaned_data['component']
                        role_component = RoleComponentsTemplate(role=role, component=component)
                        role_component.save()
            except IntegrityError:
                errors = form2._errors.setdefault("name", ErrorList())
                errors.append(u"This role already exists")

    else:
        form2 = RoleForm()
        formset = ComponentFormset()
    return render(request, 'template/role_template.html', locals())


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

    return render(request, 'add/add_host.html', locals())

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

            return redirect(host_details_2, id_host=id_host)

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

    return render(request, 'edit/edit_host.html', locals())



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



def edit_default_value(request):
    if request.is_ajax():
        new_value = request.POST['new_value']
        variable_id = request.POST['var_id']
        variable = Variable.objects.get(id=variable_id)
        variable.default_value = new_value
        variable.save()
        return HttpResponse("")
    else:
        return HttpResponse("Fail")


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
def delete_host(request, id_host):
    host = Host.objects.get(id=id_host)
    HostRole.objects.filter(host=host).delete()
    host.delete()
    return redirect(index)


# DETAILS VIEWS

def host_details(request, id_host):
    host = Host.objects.get(id=id_host)
    host_roles = HostRole.objects.filter(host=host)
    role_components = RoleComponents.objects.filter(host_role=host_roles)

    return render(request, 'details/host_details.html', locals())


def host_details_2(request, id_host):
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

    return render(request, 'details/host_details2.html', locals())


def role_details(request, id_host, id_role):
    host = Host.objects.get(id=id_host)
    role = Role.objects.get(id=id_role)
    host_role = HostRole.objects.get(host=host, role=role)
    role_components = RoleComponents.objects.filter(host_role=host_role)
    components_variables = ComponentVariables.objects.filter(role_component=role_components)

    return render(request, 'details/role_details.html', locals())


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


def autocompletion_role_name(request):
    if request.is_ajax:
        business_app = request.POST['business_app']
        ba = BusinessApplication.objects.get(name=business_app)
        prefix = ba.prefix
        data = {'prefix': prefix}
        return JsonResponse(data)
    else:
        return HttpResponse("Ramy you failed")


def save_file(request, id_host):
    host = Host.objects.get(id=id_host)
    host_roles = HostRole.objects.all().filter(host=host)
    roles_components = RoleComponents.objects.all().filter(host_role=host_roles)
    components_variables = ComponentVariables.objects.all().filter(role_component=roles_components)
    response = HttpResponse(content_type='text/txt')

    response['Content-Disposition'] = "attachment; filename=" + host.name + ".yaml"

    list = [components_variables[0]]

    for component_variable in components_variables[1:]:
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


def role_filter(request):
    if request.is_ajax:
        business_app = request.POST['business_app']
        if business_app != "--SELECT--":
            ba = BusinessApplication.objects.get(name=business_app)
            roles_ba = RoleBusinessApplication.objects.filter(business_application=ba).order_by('role')
            roles = []
            for role_ba in roles_ba:
                roles = roles + [role_ba.role]
        else:
            roles = []
        data = {}
        for role in roles:
            data[role.id] = role.name
        return JsonResponse(data)
    else:
        return HttpResponse("Ramy you failed")

