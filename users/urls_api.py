from django.urls import path
from . import views_api

urlpatterns = [
    path('users/', views_api.UserListCreateView.as_view()),
    path('users/<int:pk>/', views_api.UserRetrieveView.as_view()),
    path('auth/login/', views_api.LoginView.as_view()),
]
