from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Recipe, Evaluation

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
    fields = ['title', 'content', 'image']
    template_name = 'recipes/recipe_create_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    fields = ['title', 'content', 'image']
    template_name = 'recipes/recipe_update_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        recipe = self.get_object()
        if self.request.user == recipe.author:
            return True
        else:
            return False

class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    success_url = '/'

    def test_func(self):
        recipe = self.get_object()
        if self.request.user == recipe.author:
            return True
        else:
            return False

@login_required
def evaluate_recipe(request, pk):
    response_data = dict()
    if request.method == 'POST':
        recipe = Recipe.objects.filter(pk=pk).first()
        user = request.user
        evaluation = Evaluation.objects.filter(user=user, recipe=recipe).first()
        if evaluation:
            if request.POST['vote_or_like'] == 'like':
                if evaluation.recipce_is_liked:
                    evaluation.recipce_is_liked = False
                    recipe.like_count -= 1
                    recipe.save()
                    evaluation.save()
                    response_data = {
                        "updated_like_count": recipe.like_count
                    }
                else:
                    evaluation.recipce_is_liked = True
                    recipe.like_count += 1
                    recipe.save()
                    evaluation.save()
                    response_data = {
                        "updated_like_count": recipe.like_count
                    }
            elif 'vote' in request.POST['vote_or_like']:
                vote = int(request.POST['vote_or_like'].split("_", 1)[1])
                old_vote = evaluation.recipe_vote
                if old_vote == 0:
                    recipe.vote_count += 1
                evaluation.recipe_vote = vote
                recipe.vote_points -= old_vote
                recipe.vote_points += vote
                recipe.save()
                evaluation.save()
                response_data = {
                    "updated_vote_count": recipe.vote_count,
                    "updated_vote_ratio": int(recipe.vote_points/recipe.vote_count)
                }
        else:
            if request.POST['vote_or_like'] == 'like':
                evaluation = Evaluation(user=user, recipe=recipe, recipce_is_liked=True)
                recipe.like_count += 1
                recipe.save()
                evaluation.save()
                response_data = {
                    "updated_like_count": recipe.like_count
                }
            elif 'vote' in request.POST['vote_or_like']:
                vote = int(request.POST['vote_or_like'].split("_", 1)[1])
                evaluation = Evaluation(user=user, recipe=recipe, recipe_vote=vote)
                recipe.vote_points += vote
                recipe.vote_count += 1
                recipe.save()
                evaluation.save()
                response_data = {
                    "updated_vote_count": recipe.vote_count,
                    "updated_vote_ratio": int(recipe.vote_points/recipe.vote_count)
                }
        return JsonResponse(response_data)
