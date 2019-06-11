from django.urls import include, path
from . import views_api

urlpatterns = [
    path('users/', views_api.UserListCreateView.as_view()),
    path('auth/', include('rest_auth.urls')),
]