from django.urls import path
from . import views_api

app_name = 'api-users'

urlpatterns = [
    path('users/', views_api.UsersView.as_view(), name="users"),
    path('users/me/', views_api.MyUserDetailView.as_view(), name="my-user-detail"),
    path('auth/login/', views_api.LoginView.as_view(), name="login"),
    path('auth/change-password/', views_api.ChangePasswordView.as_view(), name="change-password"),
]
