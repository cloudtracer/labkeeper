from django import forms

from forum.models import *


class TopicForm(forms.ModelForm):
    forum = forms.ModelChoiceField(queryset=Forum.objects.all())
    subject = forms.CharField(label='Subject', max_length=255)

    class Meta:
        model = Post
        fields = ['forum', 'subject', 'body']


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['body']