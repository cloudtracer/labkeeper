from django import forms

from labs.models import ConsoleServer, ConsoleServerPort, LabProfile, Pod


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


class ConsoleServerPortForm(forms.ModelForm):

    class Meta:
        model = ConsoleServerPort
        fields = ['number', 'telnet_port', 'ssh_port']

    # Check that telnet_port and/or ssh_port is set
    def clean_ssh_port(self):

        if not self.cleaned_data['telnet_port'] and not self.cleaned_data['ssh_port']:
            raise forms.ValidationError('Please specify Telnet and/or SSH port.')

        return self.cleaned_data['ssh_port']
