from django.urls import path
from . import views

app_name = 'core_utils'

urlpatterns = [
    path('backup/', views.backup, name='backup'),
    path('attachments/', views.attachments, name='attachments'),
    path('error/', views.error, name='error'),
    path('help/', views.help, name='help'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('run/', views.run, name='run'),
]
