from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.db import transaction

from cats.models import Cat


class CatUserRegisterForm(UserCreationForm):
    name = forms.CharField(max_length=30, label='Cat Name')
    birth_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Birth Date',
    )
    personality = forms.ChoiceField(choices=Cat.PersonalityChoices.choices, label='Personality')
    photo = forms.ImageField(required=False, label='Profile photo')

    class Meta:
        model = User
        fields = ('username',)

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