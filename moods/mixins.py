from django.contrib import messages
from django.shortcuts import redirect


class UserHasCatProfileMixin:
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'cat'):
            messages.error(request, 'You need a cat profile to use the diary.')
            return redirect('home')

        return super().dispatch(request, *args, **kwargs)


class MoodEntryAccessMixin:
    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.has_perm('moods.can_view_all_moods'):
            return queryset

        if not hasattr(self.request.user, 'cat'):
            return queryset.none()

        return queryset.filter(cat=self.request.user.cat)