from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from FinalExam.Company.models import Company
from FinalExam.app_auth.models import UserProfile, Recruiters, Moderators
from django.contrib.auth.models import User

class CustomLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = ''
        self.fields['password'].label = ''

        self.fields['username'].widget.attrs['placeholder'] = "Username"
        self.fields['password'].widget.attrs['placeholder'] = "Password"


class SignUpUserForm(UserCreationForm):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = ''
        self.fields['password1'].label = ''
        self.fields['password2'].label = ''

        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'


class SignUpRecruiterForm(UserCreationForm):
    companies = forms.ModelMultipleChoiceField(queryset=Company.objects.all(), widget=forms.CheckboxSelectMultiple, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.fields['companies'].queryset.exists():
            self.fields['companies'].label = ''
            self.fields['companies'].widget = forms.TextInput(attrs={
                'placeholder': 'No companies available',
                'readonly': True})

        self.fields['username'].label = ''
        self.fields['password1'].label = ''
        self.fields['password2'].label = ''
        self.fields['companies'].label = 'Hiring For:'

        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'


class EditUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].help_text = ''

        self.fields['username'].label = 'Username'
        self.fields['first_name'].label = 'First Name'
        self.fields['last_name'].label = 'Last Name'
        self.fields['email'].label = 'Email'

        self.fields['username'].widget.attrs['placeholder'] = 'user123'
        self.fields['first_name'].widget.attrs['placeholder'] = 'John'
        self.fields['last_name'].widget.attrs['placeholder'] =  'Doe'
        self.fields['email'].widget.attrs['placeholder'] =  'john.doe@example.com'


class EditUserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['profile_picture']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['profile_picture'].label = ''

class EditModeratorForm(forms.ModelForm):
    class Meta:
        model = Moderators
        fields = ['ContactNumber']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['ContactNumber'].label = 'Contact Number'

        self.fields['ContactNumber'].widget.attrs['placeholder'] = '123-456-7890'
