from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse
from cats.models import Cat
from moods.models import MoodEntry


class MoodApiTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='12345')
        self.cat = Cat.objects.create(user=self.user, name='Tom')

        self.other_user = User.objects.create_user(username='user2', password='12345')
        self.other_cat = Cat.objects.create(user=self.other_user, name='Jerry')

        self.entry = MoodEntry.objects.create(
            cat=self.cat,
            date='2026-04-10',
            mood='happy',
            energy_level=2,
        )
        self.other_entry = MoodEntry.objects.create(
            cat=self.other_cat,
            date='2026-04-11',
            mood='sad',
            energy_level=1,
        )

    def test_anonymous_user_cannot_access_my_moods_api(self):
        response = self.client.get(reverse('api:my-mood-list'))
        self.assertEqual(response.status_code, 403)

    def test_logged_user_sees_only_own_entries_in_my_moods_api(self):
        self.client.login(username='user1', password='12345')
        response = self.client.get(reverse('api:my-mood-list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '2026-04-10')
        self.assertNotContains(response, '2026-04-11')

    def test_moderator_can_access_all_moods_api(self):
        moderator = User.objects.create_user(username='mod', password='12345')
        permission = Permission.objects.get(codename='can_view_all_moods')
        moderator.user_permissions.add(permission)

        self.client.login(username='mod', password='12345')
        response = self.client.get(reverse('api:mood-list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '2026-04-10')
        self.assertContains(response, '2026-04-11')