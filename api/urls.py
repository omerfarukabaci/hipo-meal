from django.urls import include, path
from . import views as api_views

urlpatterns = [
    path('users/', api_views.UserListView.as_view()),
    path('auth/', include('rest_auth.urls')),
]