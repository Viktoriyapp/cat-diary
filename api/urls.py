from django.urls import path
from api.views import MoodEntryApiListView, MyMoodEntryApiListView

app_name = 'api'

urlpatterns = [
    path('moods/', MoodEntryApiListView.as_view(), name='mood-list'),
path('my-moods/', MyMoodEntryApiListView.as_view(), name='my-mood-list'),
]