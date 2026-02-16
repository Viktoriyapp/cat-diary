from django.urls import path, include

from cats import views

app_name = 'cats'

urlpatterns = [
    path('', views.CatListView.as_view(), name='list'),
    path('create/', views.CatCreateView.as_view(), name='create'),

    path('<int:pk>/', include([
        path('', views.CatDetailView.as_view(), name='detail'),
        path('update/', views.CatUpdateView.as_view(), name='update'),
        path('delete/', views.CatDeleteView.as_view(), name='delete'),
    ])),

]