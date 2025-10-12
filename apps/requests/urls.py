from django.urls import path
from . import views

app_name = 'requests'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create/', views.create, name='create'),
    path('list/', views.list, name='list'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/edit/', views.edit, name='edit'),
    path('pending/', views.pending, name='pending'),
    path('templates/', views.templates_list, name='templates_list'),
]
