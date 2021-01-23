from django.urls import path
from website import views

urlpatterns = [
    path('', views.welcome, name='welcome')
]
