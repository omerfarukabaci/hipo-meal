from django.urls import path
from . import views_api

urlpatterns = [
    path('users/', views_api.UsersView.as_view()),
    path('users/me/', views_api.UserDetailView.as_view()),
    path('auth/login/', views_api.LoginView.as_view()),
    path('auth/change-password/', views_api.ChangePasswordView.as_view()),
]
