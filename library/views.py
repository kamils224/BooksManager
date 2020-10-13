from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from .models import Book
from .forms import BookForm, BookSearchForm


class BookList(generic.ListView):
    model = Book
    template_name = 'library/index.html'
    context_object_name = 'books'

    def get_queryset(self):
        title = self.request.GET.get('title', '')
        author = self.request.GET.get('author', '')
        language = self.request.GET.get('language', '')
        date_min = self.request.GET.get('release_date_min', None)
        date_max = self.request.GET.get('release_date_max', None)
        try:
            books = Book.objects.filter(title__contains=title, author__contains=author, language__contains=language)
            if date_min:
                print('None')
                books = books.filter(release_date__gt=date_min)
            if date_max:
                print('None')
                books = books.filter(release_date__lt=date_max)
            return books
        except ObjectDoesNotExist:
            return Book.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BookSearchForm()
        return context




class BookCreate(generic.CreateView):
    model = Book
    template_name = 'library/create.html'
    form_class = BookForm
    success_url = reverse_lazy('index')


class BookUpdate(generic.UpdateView):
    model = Book
    template_name = 'library/update.html'
    form_class = BookForm
    success_url = reverse_lazy('index')


class BookDelete(generic.DeleteView):
    model = Book
    success_url = reverse_lazy('index')
