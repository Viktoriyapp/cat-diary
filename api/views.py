from rest_framework.generics import ListAPIView
from api.permissions import CanViewAllMoodsPermission
from api.serializers import MoodEntrySerializer
from moods.models import MoodEntry
from rest_framework.permissions import IsAuthenticated


class MoodEntryApiListView(ListAPIView):
    queryset = MoodEntry.objects.all().order_by('-date')
    serializer_class = MoodEntrySerializer
    permission_classes = [CanViewAllMoodsPermission]


class MyMoodEntryApiListView(ListAPIView):
    serializer_class = MoodEntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if not hasattr(self.request.user, 'cat'):
            return MoodEntry.objects.none()

        return MoodEntry.objects.filter(cat=self.request.user.cat).order_by('-date')
