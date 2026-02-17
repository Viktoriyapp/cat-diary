from django.urls import path, include

from activities import views

app_name = 'activities'

urlpatterns = [
    path('', views.ActivityListView.as_view(), name='list'),
    path('create/', views.ActivityCreateView.as_view(), name='create'),
    path('<int:pk>/', include([
        path('', views.ActivityDetailView.as_view(), name='detail'),
        path('update/', views.ActivityUpdateView.as_view(), name='update'),
        path('delete/', views.ActivityDeleteView.as_view(), name='delete'),
    ]))
]