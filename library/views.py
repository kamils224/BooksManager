from django.urls import reverse_lazy
from django.views import generic

from .models import Book
from .forms import BookForm, BookSearchForm


class BookList(generic.ListView):
    model = Book
    template_name = 'library/index.html'
    context_object_name = 'books'

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
