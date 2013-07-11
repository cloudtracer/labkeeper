from django import forms

from labs.models import LabProfile, Pod


class LabProfileForm(forms.ModelForm):

    class Meta:
        model = LabProfile
        fields = ['content']


class PodForm(forms.ModelForm):

    class Meta:
        model = Pod
        fields = ['name']
