from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from cats.models import Cat
from moods.forms import MoodEntryForm
from moods.models import MoodEntry


# Create your views here.

class MoodEntryListView(ListView):
    model = MoodEntry
    template_name = 'moods/mood_list.html'
    context_object_name = 'moods'
    paginate_by = 5
    ordering = '-date'

    def get_queryset(self):
        queryset = super().get_queryset()

        cat_id = self.request.GET.get('cat') # if we have parameter cat
        mood = self.request.GET.get('mood')

        if cat_id:
            queryset = queryset.filter(cat_id=cat_id)

        if mood:
            queryset = queryset.filter(mood=mood)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['cats'] = Cat.objects.all() # for dropdown

        context['selected_cat'] = self.request.GET.get('cat')
        context['selected_mood'] = self.request.GET.get('mood')
        context['mood_choices'] = MoodEntry.MoodChoices.choices

        context['has_filters'] = bool(
            self.request.GET.get('cat') or self.request.GET.get('mood')
        ) # for button "clear filters"

        return context


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