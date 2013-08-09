from django import forms

from users.models import UserProfile


class UserProfileForm(forms.ModelForm):

    username = forms.RegexField(regex=r'^\w+$', max_length=30)
    email = forms.EmailField(label='Email address')
    password1 = forms.CharField(required=False, widget=forms.PasswordInput)
    password2 = forms.CharField(required=False, widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'birth_date', 'gender',
                  'country', 'timezone', 'location',
                  'twitter', 'facebook',
                  'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].initial = self.instance.user.username
        self.fields['email'].initial = self.instance.user.email

    def save(self, *args, **kwargs):

        # Save User attributes
        u = self.instance.user
        u.username = self.cleaned_data['username']
        u.email = self.cleaned_data['email']
        if self.cleaned_data['password1']:
            u.set_password(self.cleaned_data['password1'])
        u.save()

        return super(UserProfileForm, self).save(*args,**kwargs)

    def clean(self):
        cleaned_data = super(UserProfileForm, self).clean()

        if cleaned_data.get('password1') or cleaned_data.get('password2'):
            if cleaned_data.get('password1') != cleaned_data.get('password2'):
                msg = 'Password must be repeated twice for verification'
                self._errors['password1'] = self.error_class([msg])
                self._errors['password2'] = self.error_class([msg])

        return cleaned_data