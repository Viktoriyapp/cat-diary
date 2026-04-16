from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from cats.forms import CatForm, CatUpdateForm
from cats.models import Cat
from cats.utils import get_star_cat

class CatListView(ListView):
    model = Cat
    template_name = 'cats/cat_list.html'
    context_object_name = 'cats'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['star_cat'] = get_star_cat()
        return context


class CatDetailView(DetailView):
    model = Cat
    template_name = 'cats/cat_detail.html'
    context_object_name = 'cat'


class CatUpdateView(UpdateView):
    model = Cat
    form_class = CatUpdateForm
    template_name = 'cats/cat_update.html'
    success_url = reverse_lazy('cats:list')


class CatDeleteView(DeleteView):
    model = Cat
    template_name = 'cats/cat_confirm_delete.html'
    success_url = reverse_lazy('cats:list') #redirect after post