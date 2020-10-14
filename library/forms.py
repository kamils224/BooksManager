from bootstrap_datepicker_plus import DatePickerInput
from django import forms

from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            'release_date': DatePickerInput(format='%Y-%m-%d')
        }


class BookSearchForm(forms.Form):
    title = forms.CharField(max_length=100, required=False)
    author = forms.CharField(max_length=100, required=False)
    release_date_min = forms.DateField(widget=DatePickerInput(format='%Y-%m-%d'), required=False)
    release_date_max = forms.DateField(widget=DatePickerInput(format='%Y-%m-%d'), required=False)
    language = forms.CharField(max_length=50, required=False)


class BooksImportApiForm(forms.Form):
    q = forms.CharField(max_length=100, label='Keyword')
    intitle = forms.CharField(max_length=50, required=False)
    inauthor = forms.CharField(max_length=50, required=False)
    inpublisher = forms.CharField(max_length=50, required=False)
    subject = forms.CharField(max_length=50, required=False)
    isbn = forms.CharField(max_length=20, required=False)
    lccn = forms.CharField(max_length=50, required=False)
    oclc = forms.CharField(max_length=50, required=False)
