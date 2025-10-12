from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.list, name='list'),
    path('smart-alerts/', views.smart_alerts, name='smart_alerts'),
]
