from django import forms
from django.contrib.auth.models import User
from django_summernote.fields import SummernoteTextField
from django_summernote.widgets import SummernoteWidget

from JobPulse.Company.models import Posts, Company


class CreatePostForm(forms.ModelForm):
    Description = SummernoteTextField()

    class Meta:
        model = Posts
        fields = ['JobName', 'Description', 'Salary', 'Location', 'Seniority', 'CompanyFK']
        widgets = {
            'Description': SummernoteWidget()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['JobName'].label = ''
        self.fields['Description'].label = 'Job Description'
        self.fields['Salary'].label = ''
        self.fields['CompanyFK'].label = 'Employer'
        self.fields['Location'].label = ''


        self.fields['JobName'].widget.attrs['placeholder'] = 'Job Title'
        self.fields['Salary'].widget.attrs['placeholder'] = 'Salary'
        self.fields['Location'].widget.attrs['placeholder'] = 'Location'


class SearchForm(forms.Form):
    search_field = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Search by Post Name, Place, Seniority or Salary'}))


class EditPostForm(forms.ModelForm):
    Description = SummernoteTextField()

    class Meta:
        model = Posts
        fields = ['JobName', 'Description', 'Salary', 'Location', 'Seniority']
        widgets = {
            'Description': SummernoteWidget()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['JobName'].label = 'JobName'
        self.fields['Description'].label = 'Description'
        self.fields['Salary'].label = 'Salary'
        self.fields['Location'].label = 'Location'




class ApplyToPostForm(forms.ModelForm):

    Message = forms.CharField(widget=forms.Textarea(), required=False)
    Resume = forms.FileField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs['required'] = True
        self.fields['last_name'].widget.attrs['required'] = True
        self.fields['email'].widget.attrs['required'] = True


        self.fields['Message'].label = 'Message to the Company:'



class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'
        widgets = {
            'Description': SummernoteWidget(attrs={'style': 'width: 45%;'}),
        }
