from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from cats.models import Toy

class ToyListView(LoginRequiredMixin, ListView):
    model = Toy
    template_name = 'cats/toy_list.html'
    context_object_name = 'toys'

    def get_queryset(self):
        return Toy.objects.filter(cat=self.request.user.cat)


class ToyCreateView(LoginRequiredMixin, CreateView):
    model = Toy
    fields = ['name', 'description', 'is_favorite']
    template_name = 'cats/toy_create.html'
    success_url = reverse_lazy('cats:toy-list')

    def form_valid(self, form):
        form.instance.cat = self.request.user.cat
        return super().form_valid(form)


class ToyUpdateView(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = ['name', 'description', 'is_favorite']
    template_name = 'cats/toy_update.html'
    success_url = reverse_lazy('cats:toy-list')

    def get_queryset(self):
        return Toy.objects.filter(cat=self.request.user.cat)


class ToyDeleteView(LoginRequiredMixin, DeleteView):
    model = Toy
    template_name = 'cats/toy_confirm_delete.html'
    success_url = reverse_lazy('cats:toy-list')

    def get_queryset(self):
        return Toy.objects.filter(cat=self.request.user.cat)