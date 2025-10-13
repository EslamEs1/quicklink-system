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
    
    # إدارة القوالب
    path('templates/', views.templates_list, name='templates_list'),
    path('templates/create/', views.template_create, name='template_create'),
    path('templates/<int:pk>/edit/', views.template_edit, name='template_edit'),
    
    # إدارة أنواع الطلبات
    path('request-types/', views.request_types_list, name='request_types_list'),
    path('request-types/create/', views.request_type_create, name='request_type_create'),
    path('request-types/<int:pk>/edit/', views.request_type_edit, name='request_type_edit'),
]
