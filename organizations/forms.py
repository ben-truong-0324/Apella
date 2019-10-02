# accounts.forms.py
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import authenticate
from .models import Organization
from taggit.forms import *
#
# class OrgAddTagForm(forms.Form):
#     name = forms.CharField()
#     m_tags = TagField()

class OrgAddTagForm(forms.Form):
    tag = forms.CharField(label='Tag', max_length=100)

    # class Meta:
    #     model = Organization
    #     field = 'tags'


class RegisterForm(forms.ModelForm):

    class Meta:
        model = Organization
        fields = ('name','location_street', 'location_city',
                'location_state', 'location_country', 'location_ZIP', 'org_type',
                  )

    def clean_name(self):
        name = self.cleaned_data.get('name')
        qs = Organization.objects.filter(name=name)
        if qs.exists():
            raise forms.ValidationError("Organization may have already been registered")
        return name

    def save(self, commit=True):
        organization = super(RegisterForm, self).save(commit=False)
        organization.confirmed_identity = False #need confirmation email
        if commit:
            organization.save()
        return organization



#class RegisterImpact(forms.ModelForm):
#   add autocomplete: select2 widget


# class OrgRoleCreateForm(models.ModelForm):
#     class Meta:
#         model = OrgRole

#         def save(self,commit=True):
#             orgrole= super(OrgRoleCreateForm, self).save(commit=False)
#             if commit:
#                 orgrole.save()
#             return orgrole