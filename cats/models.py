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
    class ToyTypeChoices(models.TextChoices):
        BALL = 'ball', 'Ball'
        MOUSE = 'mouse', 'Mouse'
        FEATHER = 'feather', 'Feather'
        BOX = 'box', 'Box'
        LASER = 'laser', 'Laser'
        PLUSH = 'plush', 'Plush'
        STRING = 'string', 'String'
        HAIR_TIE = 'hair_tie', 'Hair Tie'
        SPRING = 'spring', 'Spring'
        CRINKLE = 'crinkle', 'Crinkle Toy'
        BOTTLE_CAP = 'bottle_cap', 'Bottle Cap'
        OTHER = 'other', 'Other'

    name = models.CharField(max_length=30)
    toy_type = models.CharField(max_length=20, choices=ToyTypeChoices.choices)
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