from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from cats.forms import CatForm, CatUpdateForm
from cats.models import Cat


# Create your views here.

class CatListView(ListView):
    model = Cat
    template_name = 'cats/cat_list.html'
    context_object_name = 'cats'
    paginate_by = 5


class CatDetailView(DetailView):
    model = Cat
    template_name = 'cats/cat_detail.html'
    context_object_name = 'cat'


class CatCreateView(CreateView):
    model = Cat
    form_class = CatForm
    template_name = 'cats/cat_create.html'
    success_url = reverse_lazy('cats:list')


class CatUpdateView(UpdateView):
    model = Cat
    form_class = CatUpdateForm
    template_name = 'cats/cat_update.html'
    success_url = reverse_lazy('cats:list')


class CatDeleteView(DeleteView):
    model = Cat
    template_name = 'cats/cat_confirm_delete.html'
    success_url = reverse_lazy('cats:list') #redirect after post