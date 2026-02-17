from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from moods.forms import MoodEntryForm
from moods.models import MoodEntry


# Create your views here.

class MoodEntryListView(ListView):
    model = MoodEntry
    template_name = 'moods/mood_list.html'
    context_object_name = 'moods'
    paginate_by = 2
    ordering = '-date'


class MoodEntryDetailView(DetailView):
    model = MoodEntry
    template_name = 'moods/mood_detail.html'
    context_object_name = 'mood'


class MoodEntryCreateView(CreateView):
    model = MoodEntry
    form_class = MoodEntryForm
    template_name = 'moods/mood_create.html'
    success_url = reverse_lazy('moods:list')


class MoodEntryUpdateView(UpdateView):
    model = MoodEntry
    form_class = MoodEntryForm
    template_name = 'moods/mood_update.html'
    success_url = reverse_lazy('moods:list')
    context_object_name = 'mood'


class MoodEntryDeleteView(DeleteView):
    model = MoodEntry
    template_name = 'moods/mood_confirm_delete.html'
    success_url = reverse_lazy('moods:list')
    context_object_name = 'mood'