from http.client import responses

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from cats.models import Cat
from moods.forms import MoodEntryForm
from moods.mixins import MoodEntryAccessMixin, UserHasCatProfileMixin
from moods.models import MoodEntry, DayTag
from moods.tasks import calculate_cat_statistics


class MoodEntryListView(LoginRequiredMixin, UserHasCatProfileMixin, ListView):
    model = MoodEntry
    template_name = 'moods/mood_list.html'
    context_object_name = 'moods'
    paginate_by = 5
    ordering = '-date'

    def get_queryset(self):
        queryset = super().get_queryset().filter(cat=self.request.user.cat)

        mood = self.request.GET.get('mood')
        day_tag = self.request.GET.get('day_tag')

        if mood:
            queryset = queryset.filter(mood=mood)
        if day_tag:
            queryset = queryset.filter(day_tags__id=day_tag)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['selected_mood'] = self.request.GET.get('mood')
        context['selected_day_tag'] = self.request.GET.get('day_tag')
        context['mood_choices'] = MoodEntry.MoodChoices.choices
        context['day_tags'] = DayTag.objects.order_by('name')
        context['has_filters'] = bool(self.request.GET.get('mood')
                                or self.request.GET.get('day_tag'))

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
        day_tag = self.request.GET.get('day_tag')

        if cat_id:
            queryset = queryset.filter(cat_id=cat_id)
        if mood:
            queryset = queryset.filter(mood=mood)
        if day_tag:
            queryset = queryset.filter(day_tags__id=day_tag)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['cats'] = Cat.objects.all()
        context['day_tags'] = DayTag.objects.order_by('name')
        context['selected_cat'] = self.request.GET.get('cat')
        context['selected_mood'] = self.request.GET.get('mood')
        context['selected_day_tag'] = self.request.GET.get('day_tag')
        context['mood_choices'] = MoodEntry.MoodChoices.choices
        context['has_filters'] = bool(self.request.GET.get('cat')
                                or self.request.GET.get('mood')
                                or self.request.GET.get('day_tag'))
        context['page_title'] = 'All Mood Entries'

        return context


class MoodEntryDetailView(LoginRequiredMixin, MoodEntryAccessMixin, DetailView):
    model = MoodEntry
    template_name = 'moods/mood_detail.html'
    context_object_name = 'mood'


class MoodEntryCreateView(LoginRequiredMixin, UserHasCatProfileMixin, CreateView):
    model = MoodEntry
    form_class = MoodEntryForm
    template_name = 'moods/mood_create.html'
    success_url = reverse_lazy('moods:list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.cat = self.request.user.cat
        response = super().form_valid(form)

        calculate_cat_statistics.delay(self.request.user.cat.id)
        return response


class MoodEntryUpdateView(LoginRequiredMixin,MoodEntryAccessMixin, UpdateView):
    model = MoodEntry
    form_class = MoodEntryForm
    template_name = 'moods/mood_update.html'
    success_url = reverse_lazy('moods:list')
    context_object_name = 'mood'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class MoodEntryDeleteView(LoginRequiredMixin, MoodEntryAccessMixin, DeleteView):
    model = MoodEntry
    template_name = 'moods/mood_confirm_delete.html'
    success_url = reverse_lazy('moods:list')
    context_object_name = 'mood'
