from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from activities.forms import ActivityForm
from activities.models import Activity


# Create your views here.

class ActivityListView(ListView):
    model = Activity
    template_name = 'activities/activity_list.html' #used by default, but prefer to see it
    context_object_name = 'activities'
    paginate_by = 7
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')

        if category:
            queryset = queryset.filter(category=category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_choices'] = Activity.CategoryChoices.choices
        context['selected_category'] = self.request.GET.get('category')
        return context


class ActivityDetailView(DetailView):
    model = Activity
    template_name = 'activities/activity_detail.html'
    context_object_name = 'activity'


class ActivityUpdateView(UpdateView):
    model = Activity
    template_name = 'activities/activity_update.html'
    form_class = ActivityForm
    context_object_name = 'activity'
    success_url = reverse_lazy('activities:list') #redirect


class ActivityDeleteView(DeleteView):
    model = Activity
    template_name = 'activities/activity_confirm_delete.html'
    context_object_name = 'activity'
    success_url = reverse_lazy('activities:list')


class ActivityCreateView(CreateView):
    model = Activity
    form_class = ActivityForm
    template_name = 'activities/activity_create.html'
    success_url = reverse_lazy('activities:list')