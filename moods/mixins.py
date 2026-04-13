class MoodEntryAccessMixin:
    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.has_perm('moods.can_view_all_moods'):
            return queryset

        return queryset.filter(cat=self.request.user.cat)