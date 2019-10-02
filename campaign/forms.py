# accounts.forms.py
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import authenticate
from .models import Campaign
from dal import autocomplete
from organizations.models import Organization

class RegisterCampaignForm(forms.ModelForm):

    def __init__(self, **kwargs):
        # self.organization = kwargs.pop('user', None)
        # self.organization = kwargs.pop('organization', None)

        # org_slug = kwargs.pop('org_slug', None) 
        # try:
        #     campaign.organization = Organization.objects.get(org_slug=org_slug)
        # except Organization.DoesNotExist:
        #     pass
        # # self.campaign = kwargs.pop('campaign', None)
        super(RegisterCampaignForm, self).__init__(**kwargs)

    class Meta:
        model = Campaign
        fields = ('name','summary', )
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name of campaign'}),
            'summary': forms.TextInput(attrs={'placeholder': 'Description of campaign'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        qs = Campaign.objects.filter(name=name)
        if qs.exists():
            raise forms.ValidationError("Campaign may have already been registered")
        return name
    
    # def join(request, org_slug):
    #     user = request.user
    #     org = Organization.objects.get(org_slug=org_slug)
    #     org.members.add(user)
    #     org.save()
    #     return redirect(org)
    def save(self, commit=True, **kwargs,):
        campaign = super(RegisterCampaignForm, self).save(commit=False)
        campaign.active = True #False if archived and not current
        # org_slug= self.kwargs['org_slug']

        # org_slug = kwargs.pop('org_slug', None) 
        # # org_slug=self.kwargs['org_slug']
        # try:
        #     campaign.organization = Organization.objects.get(org_slug=org_slug)
        # except Organization.DoesNotExist:
        #     pass
        if commit:
            campaign.save()
        return campaign
