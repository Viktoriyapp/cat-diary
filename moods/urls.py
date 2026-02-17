from django.urls import path, include

from moods import views

app_name = 'moods'

urlpatterns = [
    path('',views.MoodEntryListView.as_view(),name='list'),
    path('create/', views.MoodEntryCreateView.as_view(), name='create'),
    path('<int:pk>/', include([
        path('', views.MoodEntryDetailView.as_view(), name='detail'),
        path('update/', views.MoodEntryUpdateView.as_view(), name='update'),
        path('delete/', views.MoodEntryDeleteView.as_view(), name='delete'),
    ])),
]