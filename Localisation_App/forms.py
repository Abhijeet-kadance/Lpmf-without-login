from dataclasses import fields
from logging import PlaceHolder
from tkinter import Widget
from xml.dom import ValidationErr
from django import forms
from django.core import validators


'''
    AUTHOR NAME      : Shweta Patil
    CREATED DATE     : 05-07-2022
    MODEL NAME       : Registration And login
'''
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm, SetPasswordForm, UsernameField
from django.core.validators import RegexValidator


class ImageForm(forms.ModelForm):
    name = forms.CharField(label="Enter Name", widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "Enter name",'autocomplete':'off'}))
    email = forms.EmailField(label="Enter Email", widget=forms.EmailInput(
        attrs={"class": "form-control", "placeholder": "Enter email",'autocomplete':'off'}))
    phone = forms.IntegerField(label="Enter Phone No", widget=forms.NumberInput(
        attrs={"class": "form-control", "placeholder": "Enter phone no",'autocomplete':'off'}))
    password = forms.CharField(label="Enter Password", widget=forms.PasswordInput(
        attrs={"class": "form-control", "placeholder": "Enter password",'autocomplete':'off'}))
    Confirm_password = forms.CharField(label="Enter Confirm Password", widget=forms.PasswordInput(
        attrs={"class": "form-control", "placeholder": "Enter confirm password",'autocomplete':'off'}))

    class Meta:
        model = User
        fields = ['name', 'email', 'phone', 'password', 'Confirm_password']
        widget = {
            'password': forms.PasswordInput(),
            'Confirm_password': forms.PasswordInput()
        }


class ServiceForm(forms.Form):
    Language = (('English - Marathi', 'English - Marathi'),
                ('Marathi - English', 'Marathi - English'),)
    Select_Language_Pair = forms.ChoiceField(
        label='Select Language Pair', choices=Language)
    CHOICES = [('Inscript', 'Inscript'),
               ('Transliteration', 'Transliteration')]
    Keyboard = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect(attrs={"class": "form-control" ,'autocomplete':'off'}))
    inputText = forms.CharField(label='Enter text', max_length=500, widget=forms.Textarea(
        attrs={"class": "form-control", "placeholder": "Enter Text",'autocomplete':'off'}))


class TTSservice(forms.Form):
    Language = (('620fff79751fc8007d24083d', 'Hindi'), ('Tamil', 'Tamil'), ('Marathi', 'Marathi'), ('Rajasthani', 'Rajasthani'),
                ('Telugu', 'Telugu'), ('Malayalam', 'Malayalam'), ('Bengali', 'Bengali'), ('Kannada', 'Kannada'), ('Odia', 'Odia'))
    Select_Language_Pair = forms.ChoiceField(
        label='Select Language Pair', choices=Language, widget=forms.Select(attrs={'class': 'form-control','autocomplete':'off'}))
    Gernder_Select = (('male', 'Male'), ('female', 'Female'),)
    Gender = forms.ChoiceField(label='Select Gender', choices=Gernder_Select,
                               widget=forms.Select(attrs={'class': 'form-control','autocomplete':'off'}))
    InputText = forms.CharField(label='Enter text', max_length=500, widget=forms.Textarea(
        attrs={"class": "form-control", "placeholder": "Enter Text",'autocomplete':'off'}))


class TranslationQuoteForm(forms.Form):
    url = forms.URLField(validators=[validators.MaxLengthValidator(200), validators.URLValidator(
    )], required=True, widget=forms.URLInput(attrs={'class': 'form-control trans_url', 'placeholder': 'Enter URL','autocomplete':'off'}))

    company_email = forms.EmailField(validators=[validators.EmailValidator(), validators.MaxLengthValidator(
        50)], widget=forms.EmailInput(attrs={'class': 'form-control trans_email', 'placeholder': 'Enter Email','autocomplete':'off'}), required=True)

    languages = [('hindi', 'Hindi'), ('marathi', 'Marathi'), ('tamil', 'Tamil'),
                 ('bengali', 'Bengali'), ('gujarati', 'Gujarati'), ('telugu', 'Telugu')]
    language = forms.ChoiceField(validators=[validators.MaxLengthValidator(20)], required=True, help_text='Select Language',
                                 choices=languages, widget=forms.Select(attrs={'type': 'date', 'class': 'form-select trans_language','autocomplete':'off'}),)

    types = [('transport', 'Transport'), ('medical', 'Medical'), ('travel',
                                                                  'Travel and Tourism'), ('educational', 'Educational'), ('ecommerce', 'E-Commerce')]
    domain = forms.ChoiceField(validators=[validators.MaxLengthValidator(
        30)], required=True, choices=types, widget=forms.Select(attrs={'type': 'date', 'class': 'form-select trans_type','autocomplete':'off'}),)

    client_remark = forms.CharField(
        required=False, widget=forms.Textarea(
        attrs={'rows': '6', 'class': 'form-control trans_remark', 'placeholder':"Remark",'autocomplete':'off'}))

    delivery_date = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date', 'class': 'form-control trans_date','autocomplete':'off'}), required=True)
