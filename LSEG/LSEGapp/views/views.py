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
        form2 = HostForm(request.POST, auto_id=True)
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
        form2 = HostForm()
        formset = RoleFormset()

    return render(request, 'add/add_host.html', locals())


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


def add_role(request, id_host):
    return


# EDIT VIEWS
def edit_host(request, id_host):
    host = Host.objects.get(id=id_host)
    environment = host.environment
    host_roles = HostRole.objects.filter(host=host)
    list_of_roles = HostRole.objects.filter(host=host).values('role')
    RoleFormset = formset_factory(AddRoleForm)
    if request.method == 'POST':
        form2 = EnvironmentForm2(request.POST)
        form3 = HostForm(request.POST, auto_id=True)
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
        form2 = EnvironmentForm2(initial={'environment': environment})
        form3 = HostForm(initial={'name': host.name, })
        formset = RoleFormset(initial=list_of_roles)

    return render(request, 'edit/edit_host.html', locals())


def edit_role(request, id_host, id_role):
    ComponentFormset = formsets.formset_factory(AddComponentForm, extra=0)
    host = Host.objects.get(id=id_host)
    role = Role.objects.get(id=id_role)
    host_role = HostRole.objects.get(host=host, role=role)
    list_of_components = RoleComponents.objects.filter(host_role=host_role).values('component')

    if request.method == 'POST':
        RoleComponents.objects.filter(host_role=host_role).delete()
        formset = ComponentFormset(request.POST)

        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    component = form.cleaned_data['component']
                    role_component = RoleComponents(host_role=host_role, component=component)
                    role_component.save()

        return redirect(host_details, id_host=id_host)
    else:
        formset = ComponentFormset(initial=list_of_components)
        form2 = RoleForm(initial={'name': role.name})

    return render(request, 'edit/edit_role.html', locals())


def edit_role_template(request, id_role):
    ComponentFormset = formsets.formset_factory(AddComponentForm, extra=0)
    role = Role.objects.get(id=id_role)
    role_ba = RoleBusinessApplication.objects.get(role=role)
    list_of_components = RoleComponentsTemplate.objects.filter(role=role).values('component')

    if request.method == 'POST':
        form2 = RoleForm(request.POST)
        formset = ComponentFormset(request.POST)
        if form2.is_valid():
            try:
                name = form2.cleaned_data['name']
                role.name = name
                role.save()
                RoleComponentsTemplate.objects.filter(role=role).delete()
                if formset.is_valid():
                    for form in formset:
                        if form.is_valid():
                            component = form.cleaned_data['component']
                            role_component = RoleComponentsTemplate(role=role, component=component)
                            role_component.save()
                return redirect(role_template)

            except IntegrityError:
                errors = form2._errors.setdefault("name", ErrorList())
                errors.append(u"This role already exists")
    else:
        formset = ComponentFormset(initial=list_of_components)
        form2 = RoleForm(initial={'name': role.name, 'business_application': role_ba.business_application})

    return render(request, 'template/edit_role_template.html', locals())


def edit_component(request, id_host, id_role, id_component):
    host = Host.objects.get(id=id_host)
    role = Role.objects.get(id=id_role)
    host_role = HostRole.objects.get(host=host, role=role)
    component = Component.objects.get(id=id_component)
    role_component = RoleComponents.objects.get(host_role=host_role, component=component)
    VariableFormset = formsets.formset_factory(AddVariableForm, extra=0)
    list_of_variables = ComponentVariables.objects.filter(role_component=role_component).values('variable')

    if request.method == 'POST':
        ComponentVariables.objects.filter(role_component=role_component).delete()
        formset = VariableFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    variable = form.cleaned_data['variable']
                    component_variable = ComponentVariables(role_component=role_component, variable=variable)
                    component_variable.save()

        return redirect(role_details, id_host=id_host, id_role=id_role)
    else:
        formset = VariableFormset(initial=list_of_variables)

    return render(request, 'edit/edit_component.html', locals())



def edit_variable(request, id_var):
    var = Variable.objects.get(id=id_var)
    if request.method == 'POST':
        try:
            form = VariableForm(request.POST, instance=var)
            form.save()
            return redirect(variables)
        except ValueError:
            errors = form._errors.setdefault("name", ErrorList())
    else:
        form = VariableForm(instance=var)

    return render(request, 'template/edit_variable.html', locals())


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


def delete_role_template(request, id):
    try:
        role = Role.objects.get(id=id)
        role.delete()

        RoleComponentsTemplate.objects.filter(role=role).delete()

        return redirect(role_template, delete_message=1)

    except models.ProtectedError:
        return redirect(role_template, delete_message=2)


def delete_component_template(request, id):
    try:
        component = Component.objects.get(id=id)
        component.delete()

        ComponentVariablesTemplate.objects.filter(component=component).delete()
        return redirect(component_template, delete_message=1)

    except models.ProtectedError:
        return redirect(component_template, delete_message=2)


def delete_role(request, id_host, id_host_role):
    host = Host.objects.get(id=id_host)
    host_roles = HostRole.objects.all().filter(host=host)
    host_role = HostRole.objects.get(id=id_host_role)
    host_role.delete()
    if len(host_roles) == 0:
        host.delete()

    return redirect(host_details, id_host=id_host)


def delete_component(request, id_host, id_role, id_component):
    host = Host.objects.get(id=id_host)
    role = Role.objects.get(id=id_role)
    host_role = HostRole.objects.get(host=host, role=role)
    component = Component.objects.get(id=id_component)
    role_components = RoleComponents.objects.filter(host_role=host_role)
    role_component = RoleComponents.objects.get(host_role=host_role, component=component)
    role_component.delete()
    if len(role_components) == 0:
        host_role.delete()

    return redirect(role_details, id_host=id_host, id_role=id_role)


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

    role_components = roles_components[0]
    variable_list = ComponentVariables.objects.filter(role_component=role_components)
    object = [ComponentVariableList(role_component=role_components, variable_list=variable_list)]
    object_list = object_list + object
    role_component_old = role_components

    for role_components in roles_components[1:]:
        variable_list = ComponentVariables.objects.filter(role_component=role_components)
        if role_components.host_role.role.name == role_component_old.host_role.role.name:
            role_components.host_role.role.name = ""
        object = [ComponentVariableList(role_component=role_components, variable_list=variable_list)]
        object_list = object_list + object
        role_component_old = role_components

    return render(request, 'details/host_details2.html', locals())


def role_details(request, id_host, id_role):
    host = Host.objects.get(id=id_host)
    role = Role.objects.get(id=id_role)
    host_role = HostRole.objects.get(host=host, role=role)
    role_components = RoleComponents.objects.filter(host_role=host_role)
    components_variables = ComponentVariables.objects.filter(role_component=role_components)

    return render(request, 'details/role_details.html', locals())


def component_details(request, id_host, id_role, id_component):
    host = Host.objects.get(id=id_host)
    role = Role.objects.get(id=id_role)
    host_role = HostRole.objects.get(host=host, role=role)
    component = Component.objects.get(id=id_component)
    role_component = RoleComponents.objects.get(host_role=host_role, component=component)
    components_variables = ComponentVariables.objects.filter(role_component=role_component)

    return render(request, 'details/component_details.html', locals())


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

    for component_variable in components_variables:
        variable = component_variable.variable.name
        response.write(variable + ": ")
        if component_variable.value == "":
            response.write(component_variable.variable.default_value + "\n")
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

