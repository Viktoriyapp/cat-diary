from django.test import TestCase

from django.test import TestCase
from django.contrib.auth.models import User

from moods.forms import MoodEntryForm
from moods.models import MoodEntry
from cats.models import Cat
from activities.models import Activity


class MoodEntryFormTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.cat = Cat.objects.create(user=self.user, name='Tom')
        self.activity = Activity.objects.create(
            name='Sleeping',
            category='sleep',
            energy_cost=1,
        )

    def test_personal_note_too_short(self):
        form = MoodEntryForm(data={
                'date': '2026-04-10',
                'mood': 'happy',
                'energy_level': 2,
                'personal_note': 'short',
                'activities': [self.activity.id],},
            user=self.user)

        self.assertFalse(form.is_valid())
        self.assertIn('personal_note', form.errors)

    def test_sleepy_with_high_energy_invalid(self):
        form = MoodEntryForm(data={
                'date': '2026-04-10',
                'mood': 'sleepy',
                'energy_level': 3,
                'personal_note': 'This is a valid note.',
                'activities': [self.activity.id],},
            user=self.user)

        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)

    def test_duplicate_date_invalid(self):
        MoodEntry.objects.create(
            cat=self.cat,
            date='2026-04-10',
            mood='happy',
            energy_level=2,
        )

        form = MoodEntryForm(data={
                'date': '2026-04-10',
                'mood': 'sad',
                'energy_level': 1,
                'personal_note': 'Valid note here.',
                'activities': [self.activity.id],},
            user=self.user)

        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors)

    def test_same_date_different_cat_valid(self):
        other_user = User.objects.create_user(username='other', password='12345')
        other_cat = Cat.objects.create(user=other_user, name='Jerry')
        MoodEntry.objects.create(
            cat=other_cat,
            date='2026-04-10',
            mood='happy',
            energy_level=2,
        )
        form = MoodEntryForm(
            data={
                'date': '2026-04-10',
                'mood': 'sad',
                'energy_level': 1,
                'personal_note': 'Valid note here.',
                'activities': [self.activity.id],
            },
            user=self.user)

        self.assertTrue(form.is_valid())

    def test_valid_form(self):
        form = MoodEntryForm(data={
                'date': '2026-04-11',
                'mood': 'happy',
                'energy_level': 2,
                'personal_note': 'This is a valid diary note.',
                'activities': [self.activity.id],
            },
            user=self.user)

        self.assertTrue(form.is_valid())