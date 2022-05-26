from django import forms
from django.contrib.auth.models import User
from . import models

class IssueBooksForm(forms.Form):
    isbn2 = forms.ModelChoiceField(queryset=models.Book.objects.all(), empty_label="Book Name [ISBN]", to_field_name="isbn", label="Book (Name and ISBN")
    name2 = forms.ModelChoiceField(queryset=models.Member.objects.all(), empty_label="Name [Roll_on]", to_field_name="member", label="Member Details")

    isbn2.widget.attrs.update({'class' : 'form-control'})
    name2.widget.attrs.update({'class' : 'form-control'})