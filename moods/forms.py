from django import forms
from common.choices import EnergyChoices
from moods.models import MoodEntry


class MoodEntryForm(forms.ModelForm):
    class Meta:
        model = MoodEntry
        fields = '__all__'

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
            'date': forms.DateInput(attrs={'type': 'date'}),
            'personal_note': forms.Textarea(attrs={
                'placeholder': 'Today I conquered the couch and defeated the red dot!',
                'rows': 3
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields['cat'].disabled = True

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