from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    path('', views.list, name='list'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/edit/', views.edit, name='edit'),
    path('identity-check/', views.identity_check, name='identity_check'),
]
