from django.urls import path
from . import views_api

urlpatterns = [
    path('users/', views_api.UsersView.as_view(), name="api-create-user"),
    path('users/me/', views_api.UserDetailView.as_view(), name="api-edit-user"),
    path('auth/login/', views_api.LoginView.as_view(), name="api-login"),
    path('auth/change-password/', views_api.ChangePasswordView.as_view(), name="api-change-password"),
]
