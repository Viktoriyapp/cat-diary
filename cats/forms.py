from django import forms
from .models import Cat


class CatForm(forms.ModelForm):
    class Meta:
        model = Cat
        exclude = ['created_at']
        labels = {
            'name': 'My name',
            'birth_date': 'My birthday',
            'personality': 'My personality',
            'photo': 'My photo',
        }
        help_texts = {
            'name': 'What do humans usually call me?',
            'birth_date': 'If you remember it... naps can affect memory...',
            'personality': 'How would you describe yourself?',
            'photo': 'A majestic photo of me. Optional, but recommended.',
        }
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'personality': forms.Select(attrs={'class': 'form-select'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class CatUpdateForm(CatForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].disabled = True
