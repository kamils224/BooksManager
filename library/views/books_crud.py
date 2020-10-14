from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.urls import reverse_lazy
from django.views import generic

from ..forms import BookForm, BookSearchForm
from ..models import Book


class BookList(generic.ListView):
    model = Book
    template_name = 'library/index.html'
    context_object_name = 'books'

    def get_queryset(self):
        queries = self.request.GET
        if len(queries) == 0:
            return Book.objects.all()
        try:
            form = BookSearchForm(data=queries)
            books = Book.objects.filter(title__contains=form.data['title'],
                                        author__contains=form.data['author'],
                                        language__contains=form.data['language'])
            date_min = form.data.release_date_min
            date_max = form.data.release_date_max
            if date_min:
                books = books.filter(release_date__gt=date_min)
            if form.data.release_date_max:
                books = books.filter(release_date__lt=date_max)
            return books
        except ObjectDoesNotExist:
            return Book.objects.none()
        except KeyError:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = BookSearchForm()
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
