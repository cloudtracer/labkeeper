from django import forms

from labs.models import LabProfile


class LabProfileForm(forms.ModelForm):

    class Meta:
        model = LabProfile
        fields = ['content']
