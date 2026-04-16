from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from cats.models import Cat, Toy

class ToyViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='12345')
        self.cat = Cat.objects.create(user=self.user, name='Tom')

        self.other_user = User.objects.create_user(username='user2', password='12345')
        self.other_cat = Cat.objects.create(user=self.other_user, name='Jerry')

        self.toy = Toy.objects.create(
            name='Red Ball',
            description='Favorite toy',
            is_favorite=True,
            cat=self.cat,
        )

        self.other_toy = Toy.objects.create(
            name='Blue Mouse',
            description='Other cat toy',
            is_favorite=False,
            cat=self.other_cat,
        )

    def test_user_sees_only_own_toys(self):
        self.client.login(username='user1', password='12345')
        response = self.client.get(reverse('cats:toy-list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Red Ball')
        self.assertNotContains(response, 'Blue Mouse')

    def test_user_cannot_update_other_cat_toy(self):
        self.client.login(username='user1', password='12345')
        response = self.client.get(reverse('cats:toy-update', args=[self.other_toy.pk]))

        self.assertEqual(response.status_code, 404)

    def test_user_cannot_delete_other_cat_toy(self):
        self.client.login(username='user1', password='12345')
        response = self.client.get(reverse('cats:toy-delete', args=[self.other_toy.pk]))

        self.assertEqual(response.status_code, 404)