from core.mixins import MessageMixin
from core.models import Book
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class BookDetailView(DetailView):
    model = Book
    template_name = "core/book/detail.html"


class BookListView(ListView):
    model = Book
    ordering = ["name"]
    template_name = "core/book/list.html"


class BookCreateView(MessageMixin, CreateView):
    model = Book
    fields = ["name", "url", "edition", "gameline", "storytellers_vault"]
    template_name = "core/book/form.html"
    success_message = "Book created successfully."
    error_message = "Error creating book."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["url"].widget.attrs.update({"placeholder": "Enter URL here"})
        return form


class BookUpdateView(MessageMixin, UpdateView):
    model = Book
    fields = ["name", "url", "edition", "gameline", "storytellers_vault"]
    template_name = "core/book/form.html"
    success_message = "Book updated successfully."
    error_message = "Error updating book."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["url"].widget.attrs.update({"placeholder": "Enter URL here"})
        return form
