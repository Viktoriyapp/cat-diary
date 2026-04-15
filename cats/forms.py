from django import forms
from .models import Cat, Toy


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


class ToyForm(forms.ModelForm):
    class Meta:
        model = Toy
        fields = ['name', 'description', 'is_favorite']
        labels = {
            'name': 'Toy name',
            'description': 'Toy description',
            'is_favorite': 'Is this my favorite toy?',
        }
        help_texts = {
            'name': 'Give your toy a short and fun name.',
            'description': 'Optional short description of the toy.',
        }
        widgets = {
            'name': forms.TextInput(
                    attrs={'placeholder': 'Red Ball','class': 'form-control'}),
            'description': forms.Textarea(
                    attrs={'rows': 3,
                    'class': 'form-control',
                    'placeholder': 'A very bouncy toy for chaotic play sessions.',}),
            'is_favorite': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if name and len(name.strip()) < 2:
            raise forms.ValidationError('Toy name must be at least 2 characters long.')
        return name


class ToyUpdateForm(ToyForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].disabled = True