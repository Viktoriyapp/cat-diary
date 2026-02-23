from django.db import models
from common.choices import EnergyChoices
# Create your models here.

class Activity(models.Model):
    class CategoryChoices(models.TextChoices):
        PLAY = 'play', 'Play'
        SLEEP = 'sleep', 'Sleep'
        FOOD = 'food', 'Food'
        AFFECTION = 'affection', 'Affection'
        DESTRUCTION = 'destruction', 'Destruction'
        EXPLORATION = 'exploration', 'Exploration'
        WEIRD = 'weird', 'Weird'
        OBSERVATION = 'observation', 'Observation'
        TERRITORY = 'territory', 'Territory'

    name = models.CharField(max_length=50)
    category = models.CharField(choices=CategoryChoices.choices, max_length=30)
    energy_cost = models.IntegerField(choices=EnergyChoices.choices)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name