from django.urls import path, include

from cats import views, views_toy

app_name = 'cats'

toy_pk_urls = [
    path('update/', views_toy.ToyUpdateView.as_view(), name='toy-update'),
    path('delete/', views_toy.ToyDeleteView.as_view(), name='toy-delete'),
]

urlpatterns = [
    path('', views.CatListView.as_view(), name='list'),

    path('<int:pk>/', include([
        path('', views.CatDetailView.as_view(), name='detail'),
        path('update/', views.CatUpdateView.as_view(), name='update'),
        path('delete/', views.CatDeleteView.as_view(), name='delete'),
    ])),
    path('toys/', include([
        path('', views_toy.ToyListView.as_view(), name='toy-list'),
        path('create/', views_toy.ToyCreateView.as_view(), name='toy-create'),
        path('<int:pk>/', include(toy_pk_urls))
    ]))

]