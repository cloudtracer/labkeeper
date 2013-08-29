from django import forms
from django.contrib.auth.models import User

from labs.models import *


class LabForm(forms.ModelForm):

    class Meta:
        model = Lab
        fields = ['name', 'country', 'location',
                  'is_public', 'is_active', 'allow_multipod',
                  'max_rsv_per_user', 'min_reservation', 'max_reservation',
                  'opening_time', 'closing_time',
                  'photo', 'profile']

    def __init__(self, *args, **kwargs):
        super(LabForm, self).__init__(*args, **kwargs)

        # Only allow Lab to be activated if...
        if not self.instance.pods.count() or not self.instance.consoleservers.count() or not Device.objects.filter(pod__in=self.instance.pods.all()).count():
            self.fields['is_active'].widget.attrs['disabled'] = True
            self.fields['is_active'].help_text = "This lab must have at least one console server, pod, and device to be activated."


class NewLabForm(forms.ModelForm):

    class Meta:
        model = Lab
        fields = ['name', 'country', 'location', 'is_public',
                  'max_rsv_per_user', 'min_reservation', 'max_reservation',
                  'opening_time', 'closing_time']


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
    base_port_id = forms.IntegerField(min_value=0, required=False, label='Base port ID', help_text="The ID of the first port")
    base_telnet_port = forms.IntegerField(min_value=0, required=False, label='Base Telnet port', help_text="The Telnet port number of the first port")
    base_ssh_port = forms.IntegerField(min_value=0, required=False, label='Base SSH port', help_text="The SSH port number of the first port")

    def __init__(self, *args, **kwargs):
        super(NewConsoleServerForm, self).__init__(*args, **kwargs)
        self.fields['base_port_id'].widget.attrs['class'] = 'input-small'
        self.fields['base_telnet_port'].widget.attrs['class'] = 'input-small'
        self.fields['base_ssh_port'].widget.attrs['class'] = 'input-small'

    def clean(self):
        cleaned_data = super(NewConsoleServerForm, self).clean()

        # If initial port count is nonzero, base port number must be set
        if int(cleaned_data.get('port_count')):
            if not cleaned_data.get('base_port_id'):
                self._errors['base_port_id'] = self.error_class(['Must specify a base port ID'])
            if not cleaned_data.get('base_telnet_port') and not cleaned_data.get('base_ssh_port'):
                msg = 'Must specify a base Telnet and/or SSH port'
                self._errors['base_telnet_port'] = self.error_class([msg])
                self._errors['base_ssh_port'] = self.error_class([msg])

        return cleaned_data


class ConsoleServerPortForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ConsoleServerPortForm, self).__init__(*args, **kwargs)
        self.fields['number'].widget.attrs['class'] = 'input-small'
        self.fields['telnet_port'].widget.attrs['class'] = 'input-small'
        self.fields['ssh_port'].widget.attrs['class'] = 'input-small'

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


class DeviceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DeviceForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'input-block-level'
        self.fields['pod'].widget.attrs['class'] = 'input-block-level'
        self.fields['cs_port'].widget.attrs['class'] = 'input-block-level'
        self.fields['type'].widget.attrs['class'] = 'input-block-level'
        self.fields['description'].widget.attrs['class'] = 'input-block-level'

    class Meta:
        model = Device
        fields = ['name', 'pod', 'cs_port', 'type', 'description']


class MembershipManagementForm(forms.Form):

    action = forms.ChoiceField(choices=(
        ('remove', 'Remove'),
    ))

    def __init__(self, lab, *args, **kwargs):
        super(MembershipManagementForm, self).__init__(*args, **kwargs)
        self.lab = lab

        self.fields['selection'] = forms.ModelMultipleChoiceField(
            queryset = Membership.objects.filter(lab=self.lab),
            widget = forms.CheckboxSelectMultiple,
            )


class OwnerMembershipManagementForm(MembershipManagementForm):

    action = forms.ChoiceField(choices=(
        ('remove', 'Remove'),
        ('promote_admin', 'Promote to admin'),
        ('promote_owner', 'Promote to owner'),
        ('demote', 'Demote'),
    ))


class MembershipInvitationForm(forms.Form):

    member = forms.CharField(required=True)

    def __init__(self, lab, *args, **kwargs):
        super(MembershipInvitationForm, self).__init__(*args, **kwargs)
        self.lab = lab

        self.fields['member'].widget.attrs['class'] = 'input-medium'
        self.fields['member'].error_messages['required'] = "Please specify a valid username."

    def clean_member(self):
        username = self.cleaned_data['member']

        # Validate provided username
        try:
            u = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("Please specify a valid username.")

        # Check that the specified User has not already been invited to this Lab
        if MembershipInvitation.objects.filter(recipient=u, lab=self.lab):
            raise forms.ValidationError("{0} has already been invited to this lab.".format(u))

        # Check that the specified User is not already a member of this Lab
        elif Membership.objects.filter(user=u, lab=self.lab):
            raise forms.ValidationError("{0} is already a member of this lab.".format(u))

        return username


class TopologyForm(forms.ModelForm):

    class Meta:
        model = Topology
        fields = ['title', 'image']