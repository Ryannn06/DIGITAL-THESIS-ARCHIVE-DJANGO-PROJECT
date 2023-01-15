from django import forms
from .models import *
from ckeditor.widgets import CKEditorWidget
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory

import re

class AuthorForm(forms.ModelForm):
    class Meta: 
        model = Authors
        exclude = ()

        widgets = {
            'first_name': forms.TextInput(attrs=
                {'placeholder': 'First Name', 'class':'form-control', 'required':'required'}),
            'last_name': forms.TextInput(attrs=
                {'placeholder': 'Last Name', 'class':'form-control', 'required':'required'}),
            }

AuthorFormSet = inlineformset_factory(thesisDB, Authors, form=AuthorForm, 
        fields=['first_name', 'last_name',], min_num=1, validate_min=True, extra=0, can_delete=True, can_delete_extra=True)


class thesisForm(forms.ModelForm):

    class Meta:
        model = thesisDB
        fields = ('title', 'adviser','published_year','published_month', 'course','tags','abstract','pdf', 'submission_agreement',)
        readonly_fields = ['date_created']
        course = forms.ModelChoiceField(queryset=ColCourse.objects.all().order_by('-course_name'))
#        abstract = forms.CharField(widget=CKEditorWidget())
#        problem = forms.CharField(widget=CKEditorWidget())
        widgets = {
            'title': forms.TextInput(attrs=
                {'placeholder': 'Title', 'class':'form-control', 'required': 'required'}),
            'abstract': forms.Textarea(attrs=
                {'placeholder': 'Abstract', 'class':'form-control',}),
            'adviser': forms.TextInput(attrs=
                {'placeholder': 'Adviser', 'class':'form-control', 'required': 'required'}),
            'apa': forms.TextInput(attrs=
                {'placeholder': 'APA Citation Format', 'class':'form-control', 'required': 'required'}),
            'mla': forms.TextInput(attrs=
                {'placeholder': 'MLA Citation Format', 'class':'form-control', 'required': 'required'}),
            'chicago': forms.TextInput(attrs=
                {'placeholder': 'Chicago Citation Format', 'class':'form-control', 'required': 'required'}),
            'course': forms.Select(attrs=
                {'placeholder': 'Short Description', 'class':'regDropDown', 'required': 'required'}),
        }

        labels = {
            'apa': ('APA'),
            'mla': ('MLA'),
            'tags': ('Keywords'),
            'submission_agreement': ('Please check this if you agree to the terms above')
        }

    def __init__(self, *args, **kwargs):
        super(thesisForm, self).__init__(*args, **kwargs)
        # Making location required
        self.fields['pdf'].required = True
        self.fields['abstract'].required = True
        self.fields['tags'].required = True
        self.fields['submission_agreement'].required = True


class AdminthesisForm(forms.ModelForm):

    class Meta:
        model = thesisDB
        fields = ('title', 'adviser','published_year','published_month', 'course','tags','abstract','pdf',)
        readonly_fields = ['date_created']
        course = forms.ModelChoiceField(queryset=ColCourse.objects.all().order_by('-course_name'))
#        abstract = forms.CharField(widget=CKEditorWidget())
#        problem = forms.CharField(widget=CKEditorWidget())
        widgets = {
            'title': forms.TextInput(attrs=
                {'placeholder': 'Title', 'class':'form-control', 'required': 'required'}),
            'abstract': forms.Textarea(attrs=
                {'placeholder': 'Abstract', 'class':'form-control',}),
            'adviser': forms.TextInput(attrs=
                {'placeholder': 'Adviser', 'class':'form-control', 'required': 'required'}),
            'apa': forms.TextInput(attrs=
                {'placeholder': 'APA Citation Format', 'class':'form-control', 'required': 'required'}),
            'mla': forms.TextInput(attrs=
                {'placeholder': 'MLA Citation Format', 'class':'form-control', 'required': 'required'}),
            'chicago': forms.TextInput(attrs=
                {'placeholder': 'Chicago Citation Format', 'class':'form-control', 'required': 'required'}),
            'course': forms.Select(attrs=
                {'placeholder': 'Short Description', 'class':'regDropDown', 'required': 'required'}),
        }

        labels = {
            'apa': ('APA'),
            'mla': ('MLA'),
            'tags': ('Keywords'),
        }

    def __init__(self, *args, **kwargs):
        super(AdminthesisForm, self).__init__(*args, **kwargs)
        # Making location required
        self.fields['pdf'].required = True
        self.fields['abstract'].required = True
        self.fields['tags'].required = True


class EvaluateThesisForm(forms.ModelForm):
    class Meta:
        model =  thesisDB
        fields = ('published_status', 'reason', )

        widget = {
            'published_status': forms.Select(attrs=
                {'placeholder': 'Select Decision', 'class':'regDropDown', 'required': 'required'}),
            'reason': forms.Textarea(attrs=
                {'placeholder': 'Reason for Approval or Rejection', 'class':'form-control', 'required':'required'}),
        }

        labels = {
            'published_status': ('Decision'),
        }

    def __init__(self, *args, **kwargs):
        super(EvaluateThesisForm, self).__init__(*args, **kwargs)
        # Making location required
        self.fields['reason'].required = True


class departmentForm(forms.ModelForm):

    class Meta:
        model = ColDept
        fields = ('department_name', 'department_abbreviation')
        error_messages = {
            'department_name': {
                'unique': ("Department Name already exists"),
            },
            'department_abbreviation': {
                'unique': ("Department Name already exists"),
            },
        }
        widgets = {
            'department_name': forms.TextInput(attrs=
                {'placeholder': 'Department Name', 'class':'form-control', 'required': 'required'}),
            'department_abbreviation': forms.TextInput(attrs=
                {'placeholder': 'Department abbv.', 'class':'form-control', 'required': 'required'}),
        }


class courseForm(forms.ModelForm):

    class Meta:
        model = ColCourse
        fields = ('coldep_id', 'course_name', )
        coldep_id = forms.ModelChoiceField(queryset=ColDept.objects.all().order_by('-id'),)
        labels = {
            'coldep_id': ('Department'),
            'course_name': ('Program'),
        }
        error_messages = {
            'course_name': {
                'unique': ("Course Name already exists"),
            },
        }
        widgets = {
            'course_name': forms.TextInput(attrs=
                {'placeholder': 'Course Name', 'class':'form-control', 'required': 'required'}),
        }


class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(disabled=True)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name','required':'required',}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name','required':'required',}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username','required':'required',}))
    date_joined = forms.DateTimeField(disabled=True)


    class Meta:
        model = Registrations
        fields = ['username', 'email', 'first_name', 'last_name', 'date_joined']



class UpdateUserStaffForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email Address','required':'required',}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name','required':'required',}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name','required':'required',}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username','required':'required',}))
    date_joined = forms.DateTimeField(disabled=True)

    class Meta:
        model = Registrations

        fields = ['username','first_name','last_name','email', 'date_joined']


class EvaluateRequestForm(forms.ModelForm):
    class Meta:
        model = RequestPDF
        fields = ('request_status', )

        widget = {
            'request_status': forms.Select(attrs=
                {'placeholder': 'Select Decision', 'class':'regDropDown', 'required': 'required'}),
        }

        labels = {
            'request_status': ('Decision'),
        }


class SendRequestForm(forms.ModelForm):
    class Meta:
        model = RequestPDF
        fields = ('reason',)

        widgets = {
            'reason': forms.Textarea(attrs=
                {'placeholder': 'Indicate reason for access', 'class':'form-control', 'required':'required'}),
        }

    def __init__(self, *args, **kwargs):
        super(SendRequestForm, self).__init__(*args, **kwargs)
        # Making location required
        self.fields['reason'].required = True