from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    path('', views.list, name='list'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/edit/', views.edit, name='edit'),
    path('<int:pk>/export/', views.export_customer, name='export'),
    path('identity-check/', views.identity_check, name='identity_check'),
    path('identity-check/export/', views.export_conflicts, name='export_conflicts'),
    path('conflict/<int:pk>/resolve/', views.resolve_conflict, name='resolve_conflict'),
    path('conflict/<int:pk>/', views.conflict_detail, name='conflict_detail'),
]
