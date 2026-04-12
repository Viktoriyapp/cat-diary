from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from cats.models import Cat
from moods.models import MoodEntry


class Command(BaseCommand):
    help = 'Create default user groups and assign permissions'

    def handle(self, *args, **options):
        cat_users_group, _ = Group.objects.get_or_create(name='CatUsers')
        moderators_group, _ = Group.objects.get_or_create(name='Moderators')

        mood_entry_content_type = ContentType.objects.get_for_model(MoodEntry)
        cat_content_type = ContentType.objects.get_for_model(Cat)

        can_view_all_moods = Permission.objects.get(
            codename='can_view_all_moods',
            content_type=mood_entry_content_type,
        )
        can_manage_cat_profiles = Permission.objects.get(
            codename='can_manage_cat_profiles',
            content_type=cat_content_type,
        )

        moderators_group.permissions.set([
            can_view_all_moods,
            can_manage_cat_profiles,
        ])

        self.stdout.write(self.style.SUCCESS('Groups and permissions have been set up successfully.'))