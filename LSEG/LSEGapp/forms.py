from LSEGapp.models import *
from django import *
from django.forms import *
from django import forms
from django.forms.util import ErrorList


#TO ADD AN ENVIRONMENT
class EnvironmentForm(forms.Form):
    environment = forms.ModelChoiceField(queryset=Environment.objects.all(), label="Environment", widget= forms.Select(attrs={"onChange":'this.form.submit();'}), initial=1)
    #Widget option onchange that allows to sumbit the form whenever we have changed the value of the droplist


# TO ADD A HOST


class HostForm(forms.Form):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'autocomplete':'off'}))
    business_application = forms.ModelChoiceField(queryset=BusinessApplication.objects.all().order_by('name'),label="Business Application", empty_label="--SELECT--")



# TO ADD A ROLE TEMPLATE
class RoleForm(forms.Form):
    business_application = forms.ModelChoiceField(queryset=BusinessApplication.objects.all(),label="Business Application" )
    name = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'off'}))


# TO ADD A COMPONENT TEMPLATE
class ComponentForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'off'}))

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
    component = forms.ModelChoiceField(queryset=Component.objects.all(), label="Component", empty_label=None)

class AddVariableForm(forms.Form):
    variable = forms.ModelChoiceField(queryset=Variable.objects.all(), label="Variable",required=True, empty_label=None)

class AddRoleForm(forms.Form):
    role = forms.ModelChoiceField(queryset=Role.objects.all(), label="Role", empty_label=None)



class UploadFileForm(forms.Form):
    file = forms.FileField()



