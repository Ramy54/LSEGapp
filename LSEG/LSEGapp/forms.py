from LSEGapp.models import *
from django import *
from django.forms import *
from django import forms


#TO ADD AN ENVIRONMENT
class EnvironmentForm(forms.Form):
    environment = forms.ModelChoiceField(queryset=Environment.objects.all(), label="Environment", widget= forms.Select(attrs={"onChange":'this.form.submit();'}), initial=1)
    #Widget option onchange that allows to sumbit the form whenever we have changed the value of the droplist

class EnvironmentForm2(forms.Form):
    environment = forms.ModelChoiceField(queryset=Environment.objects.all(),label="Environment",initial=1)

# TO ADD A HOST
class HostForm(forms.Form):
    name = forms.CharField()
    business_application = forms.ModelChoiceField(queryset=BusinessApplication.objects.all(),label="Business Application")

# TO ADD A ROLE TEMPLATE
class RoleForm(forms.Form):
    business_application = forms.ModelChoiceField(queryset=BusinessApplication.objects.all(),label="Business Application")
    name = forms.CharField()

    def clean(self):
        cleaned_data = self.cleaned_data
        name = cleaned_data['name']

        if name and Role.objects.get(name=name):
            raise forms.ValidationError("This role already exist")

        return cleaned_data


# TO ADD A COMPONENT TEMPLATE
class ComponentForm(forms.Form):
    name = forms.CharField()

# TO ADD VARIABLES
class VariableForm(forms.ModelForm):
    class Meta:
            model = Variable
            fields = ['name','default_value','type','required','description']
            widgets = {
                'description': forms.Textarea(attrs={'rows':2,'cols':40})
            }


#FORM USED IN FORMSETS

class AddComponentForm(forms.Form):
    component = forms.ModelChoiceField(queryset=Component.objects.all(), label="Component")

class AddVariableForm(forms.Form):
    variable = forms.ModelChoiceField(queryset=Variable.objects.all(), label="Variable")

class AddRoleForm(forms.Form):
    role = forms.ModelChoiceField(queryset=Role.objects.none(), label="Role")



