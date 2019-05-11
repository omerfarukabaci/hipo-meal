from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Recipe

class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/home.html'
    context_object_name = 'recipes'
    ordering = ['-date_posted']
    # paginate_by = 

class RecipeDetailView(DetailView):
    model = Recipe

