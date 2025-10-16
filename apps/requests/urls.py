from django.urls import path
from . import views

app_name = 'requests'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('requests/create/', views.create, name='create'),
    path('requests/list/', views.list, name='list'),
    path('requests/<int:pk>/', views.detail, name='detail'),
    path('requests/<int:pk>/edit/', views.edit, name='edit'),
    path('requests/<int:pk>/delete/', views.delete, name='delete'),
    path('requests/<int:pk>/approve/', views.approve, name='approve'),
    path('requests/<int:pk>/reject/', views.reject, name='reject'),
    path('requests/<int:pk>/export-pdf/', views.export_pdf, name='export_pdf'),
    path('requests/pending/', views.pending, name='pending'),
    
    # إدارة القوالب
    path('templates/', views.templates_list, name='templates_list'),
    path('templates/create/', views.template_create, name='template_create'),
    path('templates/<int:pk>/edit/', views.template_edit, name='template_edit'),
    path('templates/<int:pk>/toggle/', views.template_toggle, name='template_toggle'),
    path('templates/<int:pk>/delete/', views.template_delete, name='template_delete'),
    
    # إدارة أنواع القوالب
    path('template-types/', views.template_types_list, name='template_types_list'),
    path('template-types/create/', views.template_type_create, name='template_type_create'),
    path('template-types/<int:pk>/edit/', views.template_type_edit, name='template_type_edit'),
    path('template-types/<int:pk>/toggle/', views.template_type_toggle, name='template_type_toggle'),
    path('template-types/<int:pk>/delete/', views.template_type_delete, name='template_type_delete'),
    
    # إدارة أنواع الطلبات
    path('request-types/', views.request_types_list, name='request_types_list'),
    path('request-types/create/', views.request_type_create, name='request_type_create'),
    path('request-types/<int:pk>/edit/', views.request_type_edit, name='request_type_edit'),
    path('request-types/<int:pk>/toggle/', views.request_type_toggle, name='request_type_toggle'),
    path('request-types/<int:pk>/delete/', views.request_type_delete, name='request_type_delete'),
    
    # إدارة فئات الطلبات
    path('requests/categories/', views.categories_list, name='categories_list'),
    path('requests/categories/create/', views.category_create, name='category_create'),
    path('requests/categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('requests/categories/<int:pk>/toggle/', views.category_toggle, name='category_toggle'),
    path('requests/categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    
    # API endpoints for sidebar counts
    path('api/pending-requests-count/', views.pending_requests_count_api, name='pending_requests_count_api'),
    path('api/notifications-count/', views.notifications_count_api, name='notifications_count_api'),
    path('api/chat-count/', views.chat_count_api, name='chat_count_api'),
]
