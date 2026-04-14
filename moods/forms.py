from django import forms
from django.core.exceptions import ValidationError

from activities.models import Activity
from common.choices import EnergyChoices
from moods.models import MoodEntry, MoodTag


class MoodEntryForm(forms.ModelForm):
    class Meta:
        model = MoodEntry
        fields = ['date', 'mood', 'energy_level', 'activities', 'personal_note']

        labels = {
            'date': 'Today`s date',
            'mood': 'How am I today?',
            'energy_level': 'How much energy do I have?',
            'activities': 'What did I do today?',
            'personal_note': 'My personal diary note'
        }

        help_texts = {
            'activities': 'Mark the activities you tackled today',
            'personal_note': 'Optional... but do share your secret thoughts'
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
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['activities'].queryset = Activity.objects.order_by('name')

    def clean_personal_note(self):
        note = self.cleaned_data.get('personal_note')

        if note and len(note.strip()) < 10:
            raise forms.ValidationError('If you`re writing a diary note, it should be at least 10 characters long.')
        return note

    def clean(self):
        cleaned_data = super().clean()

        mood = cleaned_data.get('mood')
        energy = cleaned_data.get('energy_level')

        if mood == MoodEntry.MoodChoices.SLEEPY and energy == EnergyChoices.HIGH:
            raise forms.ValidationError('If you`re sleepy, you cannot have high energy.')

        return cleaned_data


class MoodTagForm(forms.ModelForm):
    class Meta:
        model = MoodTag
        fields = ['name', 'description']

        labels = {
            'name': 'Tag name',
            'description': 'Tag description',
        }

        help_texts = {
            'name': 'Choose a short mood label such as Cozy or Zoomies.',
            'description': 'Optional short explanation of the tag.',
        }

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Cozy',
                'class': 'form-control',
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'A soft and peaceful diary tag.',
                'rows': 3,
                'class': 'form-control',
            }),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if name and len(name.strip()) < 2:
            raise forms.ValidationError('Tag name must be at least 2 characters long.')

        queryset = MoodTag.objects.filter(name__iexact=name)
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise forms.ValidationError('A tag with this name already exists.')
        return name

class MoodTagUpdateForm(MoodTagForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].disabled = True
