# accounts.forms.py
from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import authenticate
from dal import autocomplete
from django_select2.forms import Select2MultipleWidget, Select2Widget, Select2TagMixin, Select2TagWidget

from .models import  Profile
from topictag.models import Tag



class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label = 'Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username')
        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'Your e-mail'}),
            'username': forms.TextInput(attrs={'placeholder': 'Your login username'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    # if User.objects.filter(user=self.user, username=username).exists():
    #     raise forms.ValidationError("Username already exists.")

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.active = False #need confirmation email
        if commit:
            user.save()
        return user

class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class loginform(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(
        attrs={
            'placeholder':'Your login username'
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder':'Your password'
        }
    ))
    # password2 = self.cleaned_data.get("password2")
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Username or password was incorrect. Please try again.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name',
            'last_name',
            'location_city',
            'location_state',
            'location_country',
            'member_type',
            'bio',
            )
       
    def save(self, commit=True):
        profile = super(ProfileForm, self).save(commit=False)
        if commit:
            profile.save()
        return profile


    

class FollowForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('following',
        )

class UserAddTagForm(forms.Form):
    new_tag = forms.CharField(label='Tag', max_length=100)
    old_tag = forms.ModelChoiceField(
        queryset=Tag.objects.all(),
    )
