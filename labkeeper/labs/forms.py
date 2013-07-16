from django import forms

from labs.models import ConsoleServer, ConsoleServerPort, Lab, Pod


class LabForm(forms.ModelForm):

    class Meta:
        model = Lab
        fields = ['name', 'is_public', 'is_active', 'profile']


class PodForm(forms.ModelForm):

    class Meta:
        model = Pod
        fields = ['name', 'min_reservation', 'max_reservation']

    def __init__(self, *args, **kwargs):
        super(PodForm, self).__init__(*args, **kwargs)
        self.fields['min_reservation'].widget.attrs['class'] = 'input-mini'
        self.fields['max_reservation'].widget.attrs['class'] = 'input-mini'


class ConsoleServerForm(forms.ModelForm):

    class Meta:
        model = ConsoleServer
        fields = ['name', 'fqdn', 'ip4_address', 'secret']

    def clean(self):
        cleaned_data = super(ConsoleServerForm, self).clean()
        fqdn = cleaned_data.get('fqdn')
        ip4_address = cleaned_data.get('ip4_address')

        if not fqdn and not ip4_address:
            self._errors['fqdn'] = self.error_class(['Must specify a domain or IP address'])

        return cleaned_data

    # Store empty strings as NULL to bypass uniqueness check
    def clean_fqdn(self):
        return self.cleaned_data['fqdn'] or None

    # Store empty strings as NULL to bypass uniqueness check
    def clean_ip4_address(self):
        return self.cleaned_data['ip4_address'] or None


class ConsoleServerPortForm(forms.ModelForm):

    class Meta:
        model = ConsoleServerPort
        fields = ['number', 'telnet_port', 'ssh_port']

    # Check that telnet_port and/or ssh_port is set
    def clean_ssh_port(self):

        if not self.cleaned_data['telnet_port'] and not self.cleaned_data['ssh_port']:
            raise forms.ValidationError('Please specify Telnet and/or SSH port.')

        return self.cleaned_data['ssh_port']

    def clean(self):
        cleaned_data = super(ConsoleServerPortForm, self).clean()
        telnet_port = cleaned_data.get('telnet_port')
        ssh_port = cleaned_data.get('ssh_port')

        if not telnet_port and not ssh_port:
            msg = 'Must specify a Telnet and/or SSH port'
            self._errors['telnet_port'] = self.error_class([msg])
            self._errors['ssh_port'] = self.error_class([msg])

        return cleaned_data
