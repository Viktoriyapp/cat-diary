from django.db import models
from django.contrib.auth.models import User


class Cat(models.Model):
    class PersonalityChoices(models.TextChoices):
        CALM = 'calm', 'Calm'
        LAZY = 'lazy', 'Lazy'
        LOVING = 'loving', 'Loving'
        MISCHIEVOUS = 'mischievous', 'Mischievous'
        INDEPENDENT = 'independent', 'Independent'
        BAD_TEMPERED = 'bad_tempered', 'Bad tempered'
        CURIOUS = 'curious', 'Curious'
        FUN = 'fun', 'Fun'

    name = models.CharField(max_length=30)
    birth_date = models.DateField(null=True, blank=True)
    personality = models.CharField(max_length=30, choices=PersonalityChoices.choices, default=PersonalityChoices.CALM,)
    photo = models.ImageField(upload_to='cats/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        permissions = [('can_manage_cat_profiles', 'Can manage cat profiles')]

    def __str__(self):
        return self.name


class Toy(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)
    is_favorite = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    cat = models.ForeignKey(
        Cat,
        on_delete=models.CASCADE,
        related_name='toys',
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.cat.name})'