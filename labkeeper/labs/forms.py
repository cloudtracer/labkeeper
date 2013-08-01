from django import forms

from labs.models import Device, ConsoleServer, ConsoleServerPort, Lab, Pod


class LabForm(forms.ModelForm):

    class Meta:
        model = Lab
        fields = ['name', 'is_public', 'is_active', 'allow_multipod', 'min_reservation', 'max_reservation', 'opening_time', 'closing_time', 'profile']


class PodForm(forms.ModelForm):

    class Meta:
        model = Pod
        fields = ['name']


class ConsoleServerForm(forms.ModelForm):

    class Meta:
        model = ConsoleServer
        fields = ['name', 'fqdn', 'ip4_address', 'secret']

    def clean(self):
        cleaned_data = super(ConsoleServerForm, self).clean()

        # Must specify an IP address and/or domain name
        if not cleaned_data.get('fqdn') and not cleaned_data.get('ip4_address'):
            msg = 'Must specify a domain or IP address'
            self._errors['fqdn'] = self.error_class([msg])
            self._errors['ip4_address'] = self.error_class([msg])

        return cleaned_data

    # Store empty strings as NULL to bypass uniqueness check
    def clean_fqdn(self):
        return self.cleaned_data['fqdn'] or None

    # Store empty strings as NULL to bypass uniqueness check
    def clean_ip4_address(self):
        return self.cleaned_data['ip4_address'] or None


class NewConsoleServerForm(ConsoleServerForm):

    PORT_COUNT_CHOICES = (
        (0, 'None (add some later)'),
        (4, 4),
        (8, 8),
        (16, 16),
        (24, 24),
        (32, 32),
        (40, 40),
        (48, 48),
    )

    port_count = forms.ChoiceField(choices=PORT_COUNT_CHOICES, required=False)
    base_port_number = forms.IntegerField(min_value=0, help_text="The number of the first port", required=False)
    base_telnet_port = forms.IntegerField(min_value=0, help_text="The Telnet port number of the first port", required=False)
    base_ssh_port = forms.IntegerField(min_value=0, help_text="The SSH port number of the first port", required=False)

    def clean(self):
        cleaned_data = super(NewConsoleServerForm, self).clean()

        # If initial port count is nonzero, base port number must be set
        if int(cleaned_data.get('port_count')):
            if not cleaned_data.get('base_port_number'):
                self._errors['base_port_number'] = self.error_class(['Must specify a base port number'])
            if not cleaned_data.get('base_telnet_port') and not cleaned_data.get('base_ssh_port'):
                msg = 'Must specify a base Telnet and/or SSH port'
                self._errors['base_telnet_port'] = self.error_class([msg])
                self._errors['base_ssh_port'] = self.error_class([msg])

        return cleaned_data


class ConsoleServerPortForm(forms.ModelForm):

    class Meta:
        model = ConsoleServerPort
        fields = ['number', 'telnet_port', 'ssh_port']

    def clean(self):
        cleaned_data = super(ConsoleServerPortForm, self).clean()

        if not cleaned_data.get('telnet_port') and not cleaned_data.get('ssh_port'):
            msg = 'Must specify a Telnet and/or SSH port'
            self._errors['telnet_port'] = self.error_class([msg])
            self._errors['ssh_port'] = self.error_class([msg])

        return cleaned_data