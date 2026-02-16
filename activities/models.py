from django.db import models

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

        class EnergyCostChoices(models.IntegerChoices): # Not making this class reusable because its CONCEPTUALLY different from the other one in moods/models
        LOW = 1, 'Low'
        MEDIUM = 2, 'Medium'
        HIGH = 3, 'High'

    name = models.CharField(max_length=50)
    category = models.CharField(choices=CategoryChoices.choices, max_length=30)
    energy_cost = models.IntegerField(choices=EnergyCostChoices.choices)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name