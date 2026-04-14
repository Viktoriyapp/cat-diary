from django.urls import path
from api.views import MoodEntryApiListView

app_name = 'api'

urlpatterns = [
    path('moods/', MoodEntryApiListView.as_view(), name='mood-list'),
]