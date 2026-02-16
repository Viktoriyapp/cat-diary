from django.db import models

from moods.validators import date_validator


# Create your models here.

class MoodEntry(models.Model): # The mood for the day
    class MoodChoices(models.TextChoices):
        HAPPY = 'happy', 'Happy'
        SAD = 'sad', 'Sad'
        SLEEPY = 'sleepy', 'Sleepy'
        DRAMATIC = 'dramatic', 'Dramatic'
        CHAOTIC = 'chaotic', 'Chaotic'
        IRRITATED = 'irritated', 'Irritated'
        CUDDLY = 'cuddly', 'Cuddly'
        ALERT = 'alert', 'Alert'

    class EnergyLevelChoices(models.IntegerChoices): # Not making this class reusable because its CONCEPTUALLY different from the other one in activities/models
        LOW = 1, 'Low'
        MEDIUM = 2, 'Medium'
        HIGH = 3, 'High'

    date = models.DateField(validators=[date_validator])
    mood = models.CharField(max_length=30, choices=MoodChoices.choices)
    energy_level = models.IntegerField(choices=EnergyLevelChoices.choices)
    personal_note = models.TextField(null=True, blank=True)
    cat = models.ForeignKey('cats.Cat',
            on_delete=models.CASCADE,
            related_name='mood_entries') # 1 cat can have many moodEntries
    activities = models.ManyToManyField('activities.Activity',
            related_name='mood_entries',
            blank=True) # 1 moodEntry can have many activities, and 1 activity can be for many moodEntries

    def __str__(self):
        return f'{self.cat.name} - {self.date}'