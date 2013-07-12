from django import forms

from labs.models import ConsoleServer, LabProfile, Pod


class LabProfileForm(forms.ModelForm):

    class Meta:
        model = LabProfile
        fields = ['content']


class PodForm(forms.ModelForm):

    class Meta:
        model = Pod
        fields = ['name']


class ConsoleServerForm(forms.ModelForm):

    class Meta:
        model = ConsoleServer
        fields = ['name', 'fqdn', 'ip4_address', 'secret']
