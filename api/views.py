from rest_framework.generics import ListAPIView
from api.permissions import CanViewAllMoodsPermission
from api.serializers import MoodEntrySerializer
from moods.models import MoodEntry


class MoodEntryApiListView(ListAPIView):
    queryset = MoodEntry.objects.all().order_by('-date')
    serializer_class = MoodEntrySerializer
    permission_classes = [CanViewAllMoodsPermission]
