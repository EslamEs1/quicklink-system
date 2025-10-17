from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('', views.list, name='list'),
    path('process/', views.process_payment, name='process'),
    path('confirm/', views.confirm_payment, name='confirm'),
    path('cancel/', views.cancel_payment, name='cancel'),
    path('<int:payment_id>/details/', views.payment_details, name='details'),
    path('<int:payment_id>/receipt/', views.payment_receipt, name='receipt'),
    path('<int:payment_id>/send-email/', views.send_payment_email, name='send_email'),
    path('<int:payment_id>/retry/', views.retry_payment, name='retry'),
]
