from django import forms
from django.contrib.auth.models import User
from .models import Contact,Review,Checkout,Cart,Career
from django_countries.widgets import CountrySelectWidget
from django.forms import ModelForm, TextInput, NumberInput,Textarea

class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password']

class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ['author','email','phone','subject','message']


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['rating','comment','author','email','user']


class CheckoutForm(forms.ModelForm):

    class Meta:
        model = Checkout
        fields = ['country','name','username','email','address','city','state','zip_code','phone','notes']
        widgets = {'country': CountrySelectWidget()}


class DateInput(forms.DateInput):
    input_type = 'date'


class CareerForm(forms.ModelForm):

    class Meta:
        model = Career
        fields = ('name', 'father_name', 'dob', 'phone', 'email', 'address', 'profession_role', 'experience', 'message')
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'father_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Father Name'}),
            'dob': DateInput(attrs={'class':'form-control','placeholder':'Date Of Birth'}),
            'address': Textarea(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'profession_role': TextInput(attrs={'class': 'form-control', 'placeholder': 'Profession Role'}),
            'experience' : TextInput(attrs={'class': 'form-control', 'placeholder': 'Experience'}),
            'message': Textarea(attrs={'class': 'form-control', 'placeholder': 'Message for Us'}),
        }