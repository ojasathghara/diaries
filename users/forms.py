from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)  # set requierd = True if want to make compulsory

    class Meta: # this class keeps setting in one place
        model = User    # model to interact with
        fields = ['username', 'email', 'password1', 'password2'] # fields to use

    def clean_email(self):  # checks for duplicate emails
        email = self.cleaned_data.get('email')

        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return email

        # A user was found with this as a username, raise an error.
        raise forms.ValidationError('This email address is already in use.')


class UserUpdateForm(forms.ModelForm):
    # updates username and email
    
    email = forms.EmailField()  # set requierd = True if want to make compulsory

    class Meta: # this class keeps setting in one place
        model = User    # model to interact with
        fields = ['username', 'email'] # fields to use

    def clean_email(self):  # checks for duplicate emails
        old_email = self.instance.email
        email = self.cleaned_data.get('email')

        try:
            match = User.objects.get(email=email)
            if email == old_email:
                return email
        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return email

        # A user was found with this as a username, raise an error.
        raise forms.ValidationError('This email address is already in use.')

class ProfileUpdateForm(forms.ModelForm):
    # form to update profile pic
    class Meta:
        model = Profile
        fields = ['image']