from celery import shared_task
from django.db.models import Count
from moods.models import MoodEntry


@shared_task
def calculate_cat_statistics(cat_id):
    entries = MoodEntry.objects.filter(cat_id=cat_id)
    total = entries.count()
    most_common_mood = (
        entries.values('mood')
        .annotate(count=Count('mood'))
        .order_by('-count')
        .first()
    )

    return {'total_entries': total,
        'most_common_mood': most_common_mood['mood'] if most_common_mood else None}