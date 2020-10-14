from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.urls import reverse_lazy
from django.views import generic

from ..forms import BookForm, BookSearchForm
from ..models import Book
from ..filters import BookFilter


class BookList(generic.ListView):
    model = Book
    template_name = 'library/index.html'
    context_object_name = 'books'
    paginate_by = 5

    def get_queryset(self):
        qs = Book.objects.all()
        filtered_list = BookFilter(self.request.GET, queryset=qs)
        return filtered_list.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = BookSearchForm(self.request.GET)
        filter_query = self.request.GET.copy()
        filter_query.pop('page', None)
        context['filter'] = filter_query.urlencode()
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
