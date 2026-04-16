from django import forms
from activities.models import Activity
from cats.models import Toy
from common.choices import EnergyChoices
from moods.models import MoodEntry, DayTag


class MoodEntryForm(forms.ModelForm):
    class Meta:
        model = MoodEntry
        fields = ['date', 'mood', 'energy_level', 'activities', 'day_tags', 'personal_note', 'toys']
        labels = {
            'date': 'Today`s date',
            'mood': 'How am I today?',
            'energy_level': 'How much energy do I have?',
            'activities': 'What did I do today?',
            'personal_note': 'My personal diary note',
            'day_tags': 'How would I describe this day?',
            'toys': 'Which toys did I play with?'
        }

        help_texts = {
            'activities': 'Mark the activities you tackled today',
            'personal_note': 'Optional... but do share your secret thoughts',
            'day_tags': 'Optional tags that describe the vibe of the day.',
            'toys': 'Optional toys you used during the day.',
        }

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'mood': forms.Select(attrs={'class': 'form-select'}),
            'energy_level': forms.Select(attrs={'class': 'form-select'}),
            'activities': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'personal_note': forms.Textarea(attrs={
                'placeholder': 'Today I conquered the couch and defeated the red dot!',
                'rows': 3,
                'class': 'form-control',
            }),
            'day_tags': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'toys': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.fields['activities'].queryset = Activity.objects.order_by('name')
        self.fields['day_tags'].queryset = DayTag.objects.order_by('name')
        self.fields['toys'].queryset = Toy.objects.none()

        if self.user and hasattr(self.user, 'cat'):
            self.fields['toys'].queryset = Toy.objects.filter(cat=self.user.cat).order_by('name')

    def clean_personal_note(self):
        note = self.cleaned_data.get('personal_note')

        if note and len(note.strip()) < 10:
            raise forms.ValidationError('If you`re writing a diary note, it should be at least 10 characters long.')
        return note

    def clean(self):
        cleaned_data = super().clean()
        mood = cleaned_data.get('mood')
        energy = cleaned_data.get('energy_level')
        date = cleaned_data.get('date')

        if mood == MoodEntry.MoodChoices.SLEEPY and energy == EnergyChoices.HIGH:
            raise forms.ValidationError('If you`re sleepy, you cannot have high energy.')

        if self.user and hasattr(self.user, 'cat') and date:
            existing_entry = MoodEntry.objects.filter(
                cat=self.user.cat,
                date=date,
            )

            if self.instance.pk:
                existing_entry = existing_entry.exclude(pk=self.instance.pk)

            if existing_entry.exists():
                self.add_error('date', 'You already have a diary entry for this date.')

        return cleaned_data


