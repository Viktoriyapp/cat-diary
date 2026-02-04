from django.db import models

# Create your models here.

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

    def __str__(self):
        return self.name