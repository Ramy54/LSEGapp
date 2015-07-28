from django.db import models


# Environment Class
class Environment(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = '01- Environment'
        verbose_name_plural = '01- Environments'

    def __str__(self):
        return self.name


# Business Application
class BusinessApplication(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = '02- Business Application'
        verbose_name_plural = '02- Business Applications'

    def __str__(self):
        return self.name


# Host Class 
class Host(models.Model):
    name = models.CharField(max_length=50)
    environment = models.ForeignKey(Environment)

    class Meta:
        verbose_name = '03- Host'
        verbose_name_plural = '03- Hosts'

    def __str__(self):
        return self.name


# HostBusinessApplication Class
class HostBusinessApplication(models.Model):
    host = models.ForeignKey(Host)
    business_application = models.ForeignKey(BusinessApplication)

    class Meta:
        verbose_name = '04- Host Business Application'
        verbose_name_plural = '04 - Host Business Applications'

    def __str__(self):
        return self.host.name + '-' + self.business_application.name


# Role Class
class Role(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = '05- Role'
        verbose_name_plural = '05- Roles'

    def __str__(self):
        return self.name


# Component Class
class Component(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = '06- Component'
        verbose_name_plural = '06- Components'

    def __str__(self):
        return self.name


# Variable Class
class Variable(models.Model):
    name = models.CharField(max_length=50)
    default_value = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    required = models.BooleanField()
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = '07- Variable'
        verbose_name_plural = '07- Variables'

    def __str__(self):
        return self.name    


# Host Role Class
class HostRole(models.Model):
    host = models.ForeignKey(Host)
    role = models.ForeignKey(Role)

    class Meta:
        verbose_name = '08- Host Role'
        verbose_name_plural = '08- Host Roles'

    def __str__(self):
        return self.host.name + '-' + self.role.name


# Role Components Template Class
class RoleComponentsTemplate(models.Model):
    role = models.ForeignKey(Role)
    component = models.ForeignKey(Component)

    class Meta:
        verbose_name = '09- Role Components Template'
        verbose_name_plural = '09- Role Components Templates'

    def __str__(self):
        return self.role.name + '-' + self.component.name


# Component Variables Template Class
class ComponentVariablesTemplate(models.Model):
    component = models.ForeignKey(Component)
    variable = models.ForeignKey(Variable)

    class Meta:
        verbose_name = '10- Component Variables Template'
        verbose_name_plural = '10- Component Variables Templates'

    def __str__(self):
        return self.component.name + '-' + self.variable.name


# Role Components Class
class RoleComponents(models.Model):
    host_role = models.ForeignKey(HostRole)
    component = models.ForeignKey(Component)

    class Meta:
        verbose_name = '11- Role Components'
        verbose_name_plural = '11- Roles Components'

    def __str__(self):
        return self.host_role.role.name + '-' + self.component.name


# Component Variables Class
class ComponentVariables(models.Model):
    role_component = models.ForeignKey(RoleComponents)
    variable = models.ForeignKey(Variable)
    value = models.CharField(max_length=50, default="")

    class Meta:
        verbose_name = '12- Component Variables'
        verbose_name_plural = '12- Components Variables'

    def __str__(self):
        return self.role_component.component.name + '-' + self.variable.name

class ComponentVariableList:
    def __init__(self,role_component,variable_list):
        self.role_component = role_component
        self.variable_list = variable_list