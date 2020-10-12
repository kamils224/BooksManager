from datetime import datetime

from bootstrap_datepicker_plus import DatePickerInput
from django import forms
from django.forms import SelectDateWidget

from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            'release_date': DatePickerInput(format='%d/%m/%Y')
        }


class BookSearchForm(forms.Form):
    title = forms.CharField(max_length=200, required=False)
    author = forms.CharField(max_length=100, required=False)
    release_date_min = forms.DateField(widget=DatePickerInput(format='%d/%m/%Y'), required=False)
    release_date_max = forms.DateField(widget=DatePickerInput(format='%d/%m/%Y'), required=False)
    language = forms.CharField(max_length=50, required=False)

