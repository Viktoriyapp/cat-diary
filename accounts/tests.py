from django.test import TestCase

from django.test import TestCase
from django.contrib.auth.models import User, Group

from accounts.forms import CatUserRegisterForm
from cats.models import Cat


class RegisterFormTests(TestCase):

    def setUp(self):
        self.group = Group.objects.create(name='CatUsers')

    def test_register_form_valid(self):
        form = CatUserRegisterForm(
            data={
                'username': 'kitty',
                'password1': 'StrongPass123',
                'password2': 'StrongPass123',
                'name': 'Tom',
                'birth_date': '2020-01-01',
                'personality': 'calm',
            })
        self.assertTrue(form.is_valid())

    def test_register_creates_user_and_cat(self):
        form = CatUserRegisterForm(
            data={
                'username': 'kitty',
                'password1': 'StrongPass123',
                'password2': 'StrongPass123',
                'name': 'Tom',
                'birth_date': '2020-01-01',
                'personality': 'calm',
            })

        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertTrue(User.objects.filter(username='kitty').exists())
        self.assertTrue(Cat.objects.filter(user=user).exists())

    def test_user_added_to_group(self):
        form = CatUserRegisterForm(
            data={
                'username': 'kitty',
                'password1': 'StrongPass123',
                'password2': 'StrongPass123',
                'name': 'Tom',
                'birth_date': '2020-01-01',
                'personality': 'calm',
            }
        )
        user = form.save()
        self.assertTrue(user.groups.filter(name='CatUsers').exists())

    def test_password_mismatch_invalid(self):
        form = CatUserRegisterForm(
            data={
                'username': 'kitty',
                'password1': 'StrongPass123',
                'password2': 'WrongPass123',
                'name': 'Tom',
                'birth_date': '2020-01-01',
                'personality': 'calm',})

        self.assertFalse(form.is_valid())