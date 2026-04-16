from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.db import transaction
from cats.forms import CatForm
from cats.models import Cat


class CatUserRegisterForm(UserCreationForm):
    name = forms.CharField(max_length=30)
    birth_date = forms.DateField(required=False,)
    personality = forms.ChoiceField(choices=Cat.PersonalityChoices.choices,)
    photo = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        cat_form = CatForm()

        for field_name in ['name', 'birth_date', 'personality', 'photo']:
            if field_name in self.fields and field_name in cat_form.fields:
                self.fields[field_name].label = cat_form.fields[field_name].label
                self.fields[field_name].help_text = cat_form.fields[field_name].help_text
                self.fields[field_name].widget = cat_form.fields[field_name].widget

        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=commit)

        Cat.objects.create(
            user=user,
            name=self.cleaned_data['name'],
            birth_date=self.cleaned_data['birth_date'],
            personality=self.cleaned_data['personality'],
            photo=self.cleaned_data['photo'],
        )

        cat_users_group = Group.objects.filter(name='CatUsers').first()
        if cat_users_group:
            user.groups.add(cat_users_group)

        return user
