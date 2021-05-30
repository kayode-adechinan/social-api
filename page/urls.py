from django.urls import path

from . import views

urlpatterns = [
    path('send-demo-email', views.sendDemoEmail, name='send_demo_email'),
]
