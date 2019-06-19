from django.urls import path
from . import views_api

app_name = 'api-recipes'

urlpatterns = [
    path('recipes/', views_api.RecipesView.as_view(), name="recipes"),
    path('recipes/<int:pk>/', views_api.RecipesDetailView.as_view(), name="recipes-detail")
]
