from rest_framework import serializers

from moods.models import MoodEntry


class MoodEntrySerializer(serializers.ModelSerializer):
    cat_name = serializers.CharField(source='cat.name', read_only=True)
    activities = serializers.StringRelatedField(many=True)

    class Meta:
        model = MoodEntry
        fields = ['id', 'date', 'mood', 'energy_level', 'personal_note', 'cat_name', 'activities']