from django.test import TestCase

from django.test import TestCase
from django.contrib.auth.models import User, Permission

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


from django.urls import reverse


class MoodEntryViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='12345')
        self.cat = Cat.objects.create(user=self.user, name='Tom')

        self.other_user = User.objects.create_user(username='user2', password='12345')
        self.other_cat = Cat.objects.create(user=self.other_user, name='Jerry')

        self.entry = MoodEntry.objects.create(
            cat=self.cat,
            date='2026-04-10',
            mood='happy',
            energy_level=2)
        self.other_entry = MoodEntry.objects.create(
            cat=self.other_cat,
            date='2026-04-11',
            mood='sad',
            energy_level=1,
        )

    def test_login_required_for_list(self):
        response = self.client.get(reverse('moods:list'))
        self.assertEqual(response.status_code, 302)

    def test_user_sees_only_own_entries(self):
        self.client.login(username='user1', password='12345')
        response = self.client.get(reverse('moods:list'))

        self.assertContains(response, f'/moods/{self.entry.pk}/')
        self.assertNotContains(response, f'/moods/{self.other_entry.pk}/')

    def test_user_cannot_access_other_entry_detail(self):
        self.client.login(username='user1', password='12345')

        response = self.client.get(
            reverse('moods:detail', args=[self.other_entry.pk])
        )
        self.assertEqual(response.status_code, 404)

    def test_user_can_access_own_entry_detail(self):
        self.client.login(username='user1', password='12345')

        response = self.client.get(
            reverse('moods:detail', args=[self.entry.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_moderator_can_access_all_entries(self):
        moderator = User.objects.create_user(username='mod', password='12345')
        moderator.is_staff = True
        moderator.save()

        permission = Permission.objects.get(codename='can_view_all_moods')
        moderator.user_permissions.add(permission)

        self.client.login(username='mod', password='12345')
        response = self.client.get(reverse('moods:all'))
        self.assertEqual(response.status_code, 200)