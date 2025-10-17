from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('', views.list, name='list'),
    path('process/', views.process_payment, name='process'),
    path('<int:pk>/details/', views.payment_details, name='details'),
    path('<int:pk>/receipt/', views.payment_receipt, name='receipt'),
    path('<int:pk>/confirm/', views.confirm_payment, name='confirm'),
    path('<int:pk>/cancel/', views.cancel_payment, name='cancel'),
    path('<int:pk>/retry/', views.retry_payment, name='retry'),
    path('<int:pk>/send-email/', views.send_payment_email, name='send_email'),
]
