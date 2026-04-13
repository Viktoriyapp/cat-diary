from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from cats.models import Cat
from moods.forms import MoodEntryForm
from moods.models import MoodEntry


# Create your views here.

class MoodEntryListView(LoginRequiredMixin, ListView):
    model = MoodEntry
    template_name = 'moods/mood_list.html'
    context_object_name = 'moods'
    paginate_by = 5
    ordering = '-date'

    def get_queryset(self):
        queryset = super().get_queryset().filter(cat=self.request.user.cat)

        mood = self.request.GET.get('mood')

        if mood:
            queryset = queryset.filter(mood=mood)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['cats'] = Cat.objects.filter(user=self.request.user)

        context['selected_cat'] = str(self.request.user.cat.pk)
        context['selected_mood'] = self.request.GET.get('mood')
        context['mood_choices'] = MoodEntry.MoodChoices.choices

        context['has_filters'] = bool(self.request.GET.get('mood'))

        return context


class AllMoodEntryListView(PermissionRequiredMixin, ListView):
    model = MoodEntry
    template_name = 'moods/mood_all_list.html'
    context_object_name = 'moods'
    paginate_by = 5
    ordering = '-date'
    permission_required = 'moods.can_view_all_moods'

    def get_queryset(self):
        queryset = super().get_queryset()

        cat_id = self.request.GET.get('cat')
        mood = self.request.GET.get('mood')

        if cat_id:
            queryset = queryset.filter(cat_id=cat_id)

        if mood:
            queryset = queryset.filter(mood=mood)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['cats'] = Cat.objects.all()
        context['selected_cat'] = self.request.GET.get('cat')
        context['selected_mood'] = self.request.GET.get('mood')
        context['mood_choices'] = MoodEntry.MoodChoices.choices
        context['has_filters'] = bool(self.request.GET.get('cat') or self.request.GET.get('mood'))
        context['page_title'] = 'All Mood Entries'

        return context


class MoodEntryDetailView(LoginRequiredMixin, DetailView):
    model = MoodEntry
    template_name = 'moods/mood_detail.html'
    context_object_name = 'mood'

    def get_queryset(self):
        return super().get_queryset().filter(cat=self.request.user.cat)


class MoodEntryCreateView(LoginRequiredMixin, CreateView):
    model = MoodEntry
    form_class = MoodEntryForm
    template_name = 'moods/mood_create.html'
    success_url = reverse_lazy('moods:list')

    def form_valid(self, form):
        form.instance.cat = self.request.user.cat
        return super().form_valid(form)


class MoodEntryUpdateView(LoginRequiredMixin, UpdateView):
    model = MoodEntry
    form_class = MoodEntryForm
    template_name = 'moods/mood_update.html'
    success_url = reverse_lazy('moods:list')
    context_object_name = 'mood'

    def get_queryset(self):
        return super().get_queryset().filter(cat=self.request.user.cat)


class MoodEntryDeleteView(LoginRequiredMixin, DeleteView):
    model = MoodEntry
    template_name = 'moods/mood_confirm_delete.html'
    success_url = reverse_lazy('moods:list')
    context_object_name = 'mood'

    def get_queryset(self):
        return super().get_queryset().filter(cat=self.request.user.cat)