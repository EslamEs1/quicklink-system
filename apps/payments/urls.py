from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('', views.list, name='list'),
    path('process/', views.process_payment, name='process'),
]
