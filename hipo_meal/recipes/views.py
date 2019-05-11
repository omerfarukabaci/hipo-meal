from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Recipe

class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/home.html'
    context_object_name = 'recipes'
    ordering = ['-date_posted']
    paginate_by = 3

class RecipeDetailView(DetailView):
    model = Recipe

class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    fields = ['title', 'content']
    template_name = 'recipes/recipe_create_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipe
    fields = ['title', 'content']
    template_name = 'recipes/recipe_update_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)