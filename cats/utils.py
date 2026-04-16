from django.db.models import Count
from cats.models import Cat


def get_star_cat():
    star_cat = (Cat.objects
        .annotate(entries_count=Count('mood_entries'))
        .order_by('-entries_count').first())

    if star_cat and star_cat.entries_count > 0:
        return star_cat
    return None