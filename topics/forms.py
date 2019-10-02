# accounts.forms.py
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import authenticate
from .models import Topic, ExplorePost
from dal import autocomplete
from organizations.models import Organization



class RegisterTopicForm(forms.ModelForm):

    def __init__(self, **kwargs):
        # self.organization = kwargs.pop('user', None)
        self.organization = kwargs.pop('organization', None)
        self.topic = kwargs.pop('topic', None)
        super(RegisterTopicForm, self).__init__(**kwargs)

    class Meta:
        model = Topic
        fields = ('name','summary', )
           
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name of topic'}),
            'summary': forms.TextInput(attrs={'placeholder': 'Description of topic'}),

        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        qs = Topic.objects.filter(name=name)
        if qs.exists():
            raise forms.ValidationError("Topic may have already been registered")
        return name

    def save(self, commit=True):
        topic = super(RegisterTopicForm, self).save(commit=False)
        topic.active = True #False if archived and not current
        topic.organization = self.organization
        # topic.organization = Organization.objects.get(slug=self.kwargs['org_slug'])
        if commit:
            topic.save()
        return topic

class TopicAddTagForm(forms.Form):
    tag = forms.CharField(label='Tag', max_length=100)

class ExplorePostAddForm(forms.ModelForm):

    def __init__(self, **kwargs):
        self.user = kwargs.pop('user', None)
        self.topic = kwargs.pop('topic', None)
        super(ExplorePostAddForm, self).__init__(**kwargs)

    def save(self, commit=True):
        obj = super(ExplorePostAddForm, self).save(commit=False)
        obj.user = self.user
        obj.topic = self.topic
        if commit:
            obj.save()
        return obj
    class Meta:
        model = ExplorePost
        fields = ('content',)
        widgets = {
            'content': forms.TextInput(attrs={'placeholder': 'Content of statement'}),
        }
        #field of topic is automatically added by url and creator user