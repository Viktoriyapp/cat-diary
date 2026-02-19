from django import forms

from activities.models import Activity


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['name', 'category', 'energy_cost', 'description']

        labels ={
            'name': 'What did I do?',
            'category': 'What kind of activity was it?',
            'energy_cost': 'How tiring was it for me?',
            'description': 'Tell the story'
        }

        help_texts = {
            'description': 'Describe adventure in more detail.',
        }

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Chased invisible entities.',
                'class': 'form-control',
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
            }),
            'energy_cost': forms.Select(attrs={
                'class': 'form-select',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows':3
            }),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if len(name) < 3:
            raise forms.ValidationError(
                'Activity name must be at least 3 characters long.'
            )
        return name