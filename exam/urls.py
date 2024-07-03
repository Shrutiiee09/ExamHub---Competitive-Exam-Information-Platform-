from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/exams/', views.api_exams, name='api_exams'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('logout/', views.custom_logout, name='logout'),
    path('feedback/', views.feedback_page, name='feedback'),
]
