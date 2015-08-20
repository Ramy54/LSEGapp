__author__ = 'ramyah'

from django.http import *
from django.shortcuts import *
from LSEGapp.forms import *
from LSEGapp.models import *
from django.forms.formsets import *
from django.db import IntegrityError
from django.forms.utils import ErrorList



# MAIN VIEW TO RENDER THE ROLE_TEMPLATE (/role_template URL)
def role_template(request):
    return render(request, 'template/roles/role_template.html', locals())

def get_roles(request):
    if request.is_ajax:

        role_filter = request.POST['role_filter']
        roles_components = RoleComponentsTemplate.objects.all().order_by('role__name')
        if role_filter != "":
            roles = Role.objects.all().filter(name__contains=role_filter)
            roles_components = roles_components.filter(role=roles)

        dict ={}
        roles_components_list = []

        if roles_components.exists():
            role_component = roles_components[0]
            role_component_old = roles_components[0]
            component_text = '<a href="/component_template">' + role_component_old.component.name + '</a>'

            for role_component in roles_components[1:]:
                if role_component.role.name == role_component_old.role.name:
                    component_text = component_text + '<br><a href="/component_template">' + role_component.component.name + '</a>'
                else:
                    record = {'id': role_component_old.role.id, 'role':role_component_old.role.name,'component_text': component_text}
                    roles_components_list.append(record)
                    component_text= '<a href="/component_template">' + role_component.component.name + '</a>'
                role_component_old = role_component

            if role_component.role.name == role_component_old.role.name:
                component_text = component_text
                record = {'id': role_component_old.role.id, 'role': role_component_old.role.name,'component_text': component_text}
                roles_components_list.append(record)

        dict['roles_components'] = roles_components_list
        return JsonResponse(dict)
    else:
        return HttpResponse("You failled")


# ADD A ROLE VIEW (HAS ITS OWN URL)
def add_role_template(request):
    ComponentFormset = formset_factory(AddComponentForm)
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
                return  redirect(role_template)
            except IntegrityError:
                errors = form2._errors.setdefault("name", ErrorList())
                errors.append(u"This role already exists")
    else:
        form2 = RoleForm()
        formset = ComponentFormset()
    return render(request, 'template/roles/add_role_template.html', locals())


# EDIT A ROLE VIEW (HAS ITS OWN URL)
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

    return render(request, 'template/roles/edit_role_template.html', locals())


def delete_role_template(request):
    if request.is_ajax:
        role_name = request.POST['role_name']
        role = Role.objects.get(name=role_name)
        role.delete()
        return HttpResponse('Success')

    else:
        return HttpResponse('You Failed')


def is_role_used(request):
    if request.is_ajax:
        role_name = request.POST['role_name']
        role = Role.objects.get(name=role_name)
        host_roles = HostRole.objects.filter(role=role)
        if not(host_roles.exists()):
            used = False
            return JsonResponse({'boolean': used})

        else:
            used = True
            message = "The role " + role.name + " is used"
            return JsonResponse({'boolean': used, 'message':message})
    else:
        return HttpResponse('You Failled')


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