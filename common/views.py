from django.db.models import Count, Avg
from django.shortcuts import render
from django.views.generic import TemplateView

from cats.models import Cat
from moods.models import MoodEntry


# Create your views here.

class HomePageView(TemplateView):
    template_name = 'common/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total_cats = Cat.objects.count()
        total_entries = MoodEntry.objects.count()
        most_active_cat = (Cat.objects
                .annotate(entries_count=Count('mood_entries'))
                .order_by('-entries_count')
                .first()
            )
        context.update({
            'total_cats': total_cats,
            'total_entries': total_entries,
            'most_active_cat': most_active_cat,
        })

        return context


def custom_404(request, exception):
    return render(request, 'common/404.html', status=404)