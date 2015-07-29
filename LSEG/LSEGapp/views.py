from django.http import *
import csv
from django.shortcuts import *
from LSEGapp.forms import *
from LSEGapp.models import *
from django.forms.formsets import *
from django.core.files import File

# MAIN PAGES VIEWS
def bootstrap(request):
    return render(request, 'bootstrap.html')

def index(request):
    environment = Environment.objects.first()
    if request.method == 'POST': # If the form has been submitted...
        form = EnvironmentForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            environment = form.cleaned_data['environment']

    else:
        form = EnvironmentForm()

    hosts = Host.objects.filter(environment=environment)
    host_roles =[]
    for host in hosts:
        host_roles = host_roles + list(HostRole.objects.filter(host=host))

    return render(request, 'index.html', locals())

def skeleton(request):
    return render(request, "skeleton.html")



# TEMPLATE VIEWS
def role_template(request):
    ComponentFormset = formset_factory(AddComponentForm)
    roles_components = RoleComponentsTemplate.objects.all()

    if request.method == 'POST':
        form2 = RoleForm(request.POST)
        formset = ComponentFormset(request.POST)

        if form2.is_valid():
            if formset.is_valid():
                name = form2.cleaned_data['name']    #Get name from the form
                role = Role(name=name)
                role.save()

                for form in formset:
                    component = form.cleaned_data['component']
                    role_component = RoleComponentsTemplate(role=role,component=component)
                    role_component.save()

    else:
        form2 = RoleForm()
        formset = ComponentFormset()
    return render(request, 'temp/role_template.html',locals())

def component_template(request):
    VariableFormset = formsets.formset_factory(AddVariableForm)
    components_variables = ComponentVariablesTemplate.objects.all()

    if request.method == 'POST':
        form2 = ComponentForm(request.POST)
        formset = VariableFormset(request.POST)

        if form2.is_valid():
            name = form2.cleaned_data['name']    #Get name from the form
            component = Component(name=name)
            component.save()
            if formset.is_valid():
                for form in formset:
                    var = form.cleaned_data['variable']
                    component_variable = ComponentVariablesTemplate(component=component, variable=var)
                    component_variable.save()

    else:
        form2 = ComponentForm()
        formset = VariableFormset()

    return render(request, 'temp/component_template.html',locals())

def variables(request):
    variables = Variable.objects.all()  #The variables to be given to the template

    if request.method == 'POST':
        form = VariableForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            default_value = form.cleaned_data['default_value']
            type = form.cleaned_data['type']
            required = form.cleaned_data['required']
            description = form.cleaned_data['description']

            new_var = Variable(name=name,default_value=default_value,type=type,required=required,description=description)
            new_var.save()
    else:
        form = VariableForm()

    return render(request, 'temp/variables.html', locals())



# ADD VIEWS
def add_host(request,id_env):
    RoleFormset = formset_factory(AddRoleForm)
    environment = Environment.objects.get(id=id_env)
    if request.method == 'POST':
        form2 = HostForm(request.POST, auto_id=True )
        formset = RoleFormset(request.POST)

        if form2.is_valid():

            if formset.is_valid():
                name = form2.cleaned_data['name']    #Get name from the form
                business_application = form2.cleaned_data['business_application']
                host = Host(name=name, environment=environment)
                host.save()                         #Add a host
                host_business_application = HostBusinessApplication(business_application=business_application,host=host)
                host_business_application.save()    #Add a host_business_app

                roles_id = []

                for form in formset:
                    role = form.cleaned_data['role']
                    id = [role.id]
                    roles_id = roles_id + id

                save_roles(host,roles_id)
                return redirect(index)

    else:
        form2 = HostForm()
        formset = RoleFormset()

    return render(request, 'add/add_host.html', locals(), context_instance=RequestContext(request))

def save_roles(host,roles_id):

    for role_id in roles_id:
        host_role = HostRole(host=host,role=Role.objects.get(id=role_id))
        host_role.save()                    #Add a host role
        role_components_template = RoleComponentsTemplate.objects.filter(role=Role.objects.get(id=role_id))

        for role_component_template in role_components_template: #THIS LOOP ADDS THE DIFFERENT COMPONENTS OF A TEMPLATE ROLE
            component = role_component_template.component
            role_component = RoleComponents(host_role=host_role,component=component)
            role_component.save() #Save the role_component generated from the template
            component_variables_template = ComponentVariablesTemplate.objects.filter(component=Component.objects.get(name=component.name))

            for component_variable_template in component_variables_template: #THIS LOOP ADDS THE DIFFERENT VARIABLES OF A COMPONENT TEMPLATE
                variable = component_variable_template.variable
                component_variable = ComponentVariables(role_component=role_component,variable=variable)
                component_variable.save()

def add_role(request,id_host):
    return


# EDIT VIEWS
def edit_host(request,id_host):
    RoleFormset = formset_factory(AddRoleForm,extra=0)
    host = Host.objects.get(id=id_host)
    environment = host.environment
    host_business_application = HostBusinessApplication.objects.get(host=host)
    host_roles = HostRole.objects.filter(host=host)
    list_of_roles = HostRole.objects.filter(host=host).values('role')

    if request.method == 'POST':
        form2 = EnvironmentForm2(request.POST)
        form3 = HostForm( request.POST, auto_id=True )
        formset = RoleFormset(request.POST)
        host_roles.delete()
        if form2.is_valid():
            environment = form2.cleaned_data['environment']
            host.environment = environment
            if form3.is_valid():
                name = form3.cleaned_data['name']
                host.name = name
                host.save()
                business_application = form3.cleaned_data['business_application']
                host_business_application.business_application = business_application
                host_business_application.save()
                if formset.is_valid():
                    roles_id = []
                    for form in formset:
                        role = form.cleaned_data['role']
                        id = [role.id]
                        roles_id = roles_id + id

                    save_roles(host,roles_id)

                return redirect(index)

    else:
        form2 = EnvironmentForm2(initial={'environment': environment})
        form3 = HostForm(initial={'name':host.name,'business_application':host_business_application.business_application})
        formset = RoleFormset(initial=list_of_roles)

    return render(request, 'edit/edit_host.html', locals())

def edit_role(request,id_host,id_role):
    ComponentFormset = formsets.formset_factory(AddComponentForm,extra=0)
    host = Host.objects.get(id=id_host)
    role = Role.objects.get(id=id_role)
    host_role = HostRole.objects.get(host=host,role=role)
    list_of_components = RoleComponents.objects.filter(host_role=host_role).values('component')

    if request.method == 'POST':
        RoleComponents.objects.filter(host_role=host_role).delete()
        formset = ComponentFormset(request.POST)

        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    component = form.cleaned_data['component']
                    role_component = RoleComponents(host_role=host_role , component=component)
                    role_component.save()

        return redirect(host_details,id_host=id_host)
    else:
        formset = ComponentFormset(initial=list_of_components)
        form2 = RoleForm(initial={'name':role.name})

    return render(request, 'edit/edit_role.html',locals())


def edit_role_template(request, id_role):
    ComponentFormset = formsets.formset_factory(AddComponentForm,extra=0)
    role = Role.objects.get(id=id_role)
    list_of_components = RoleComponentsTemplate.objects.filter(role=role).values('component')

    if request.method == 'POST':
        RoleComponentsTemplate.objects.filter(role=role).delete()
        form2 = RoleForm(request.POST)
        formset = ComponentFormset(request.POST)
        if form2.is_valid():
            name = form2.cleaned_data['name']
            role.name = name
            role.save()
        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    component = form.cleaned_data['component']
                    role_component = RoleComponentsTemplate(role=role , component=component)
                    role_component.save()

        return redirect(role_template)
    else:
        formset = ComponentFormset(initial=list_of_components)
        form2 = RoleForm(initial={'name':role.name})

    return render(request, 'temp/edit_role_template.html',locals())

def edit_component(request,id_host,id_role,id_component):
    host = Host.objects.get(id=id_host)
    role = Role.objects.get(id=id_role)
    host_role = HostRole.objects.get(host=host,role=role)
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
                    component_variable = ComponentVariables(role_component=role_component , variable=variable)
                    component_variable.save()

        return redirect(role_details,id_host=id_host,id_role=id_role)
    else:
        formset = VariableFormset(initial=list_of_variables)

    return render(request,'edit/edit_component.html' , locals())


def edit_component_template(request,id_component):
    VariableFormset = formsets.formset_factory(AddVariableForm, extra=0)
    component = Component.objects.get(id=id_component)
    list_of_variables = ComponentVariablesTemplate.objects.filter(component=component).values('variable')

    if request.method == 'POST':
        ComponentVariablesTemplate.objects.filter(component=component).delete()
        form2 = ComponentForm(request.POST)
        formset = VariableFormset(request.POST)
        if form2.is_valid():
            name = form2.cleaned_data['name']
            component.name=name
            component.save()
        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    variable = form.cleaned_data['variable']
                    component_variable = ComponentVariablesTemplate(component=component,variable=variable)
                    component_variable.save()

        return redirect(component_template)
    else:
        formset = VariableFormset(initial=list_of_variables)
        form2 = ComponentForm(initial={'name': component.name})

    return render(request, 'temp/edit_component_template.html',locals())

def edit_variable(request,id_var):
    var = Variable.objects.get(id=id_var)
    if request.method == 'POST':
        form = VariableForm(request.POST,instance=var)
        form.save()
        return redirect(variables)
    else:
        form= VariableForm(instance=var)

    return render(request, 'temp/edit_variable.html',locals())




# DELETE METHODS/VIEWS
def delete_host(request,id_host):
    host = Host.objects.get(id=id_host)
    host.delete()
    return redirect(index)

def delete_role_template(request,id):
    role = Role.objects.get(id=id)
    role.delete()
    return redirect(role_template)

def delete_component_template(request,id):
    component = Component.objects.get(id=id)
    component.delete()
    return redirect(component_template)

def delete_variable(request,id):
    var = Variable.objects.get(id=id)
    var.delete()
    return redirect(variables)

def delete_role(request,id_host,id_host_role):
    host = Host.objects.get(id=id_host)
    host_roles = HostRole.objects.all().filter(host=host)
    host_role = HostRole.objects.get(id=id_host_role)
    host_role.delete()
    if len(host_roles)==0:
        host.delete()

    return redirect(host_details,id_host=id_host)

def delete_component(request,id_host,id_role,id_component):
    host= Host.objects.get(id=id_host)
    role = Role.objects.get(id=id_role)
    host_role = HostRole.objects.get(host=host,role=role)
    component = Component.objects.get(id=id_component)
    role_components = RoleComponents.objects.filter(host_role=host_role)
    role_component = RoleComponents.objects.get(host_role=host_role, component=component)
    role_component.delete()
    if len(role_components)==0:
        host_role.delete()

    return redirect(role_details,id_host=id_host,id_role=id_role)


# DETAILS VIEWS

def host_details(request,id_host):
    host = Host.objects.get(id=id_host)
    host_roles = HostRole.objects.filter(host=host)
    role_components = []

    for host_role in host_roles:
        role_components = role_components + list(RoleComponents.objects.filter(host_role=host_role))

    return render(request, 'details/host_details.html',locals())

def role_details(request,id_host,id_role):
    host = Host.objects.get(id=id_host)
    role = Role.objects.get(id=id_role)
    host_role = HostRole.objects.get(host=host,role=role)
    role_components = RoleComponents.objects.filter(host_role=host_role)

    components_variables = []
    for role_component in role_components:
        components_variables = components_variables + list(ComponentVariables.objects.filter(role_component=role_component))

    return render(request, 'details/role_details.html',locals())

def component_details(request,id_host,id_role,id_component):
    host = Host.objects.get(id=id_host)
    role = Role.objects.get(id=id_role)
    host_role = HostRole.objects.get(host=host,role=role)
    component = Component.objects.get(id=id_component)
    role_component = RoleComponents.objects.get(host_role=host_role,component=component)
    components_variables = ComponentVariables.objects.filter(role_component=role_component)

    return render(request, 'details/component_details.html',locals())


# DISPLAY USED FOR JAVASCRIPT RENDERING OF FORMSET
def display_data(request, data, **kwargs):
    return render_to_response('posted-data.html', dict(data=data, **kwargs),
                              context_instance=RequestContext(request))



def save_file(request,id_host):
    host = Host.objects.get(id=id_host)
    host_roles = HostRole.objects.all().filter(host=host)
    roles_components = RoleComponents.objects.all().filter(host_role = host_roles)
    components_variables = ComponentVariables.objects.all().filter(role_component = roles_components)
    response = HttpResponse(content_type='text/txt')

    response['Content-Disposition'] = "attachment; filename=" + host.name + ".yaml"

    for component_variable in components_variables:
        variable = component_variable.variable.name
        response.write(variable + ": " + component_variable.variable.default_value + "\n")

    return response


def edit_value(request):
    if request.is_ajax:
        new_value = request.POST['new_value']
        component_var_id = request.POST['component_var_id']
        component_variable = ComponentVariables.objects.get(id=component_var_id)
        component_variable.value = new_value
        component_variable.save()
        return HttpResponse("")
    else:
        return HttpResponse("FAIL")
