from django.urls import path
from . import views

app_name = 'settings_app'

urlpatterns = [
    path('', views.general, name='general'),
    path('users/', views.users, name='users'),
    path('permissions/', views.permissions, name='permissions'),
]
