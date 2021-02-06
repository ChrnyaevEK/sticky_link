from django.urls import path
from website import views

urlpatterns = [
    path('', views.index, name='website'),
    path('profile/', views.profile, name='profile')
]
