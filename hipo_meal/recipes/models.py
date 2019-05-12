from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from PIL import Image, ImageOps

class Ingredient(models.Model):
    name = models.CharField(max_length=75, unique=True)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    DIFFICULTY_CHOICES = [
        ("1", "Easy"),
        ("2", "Medium"),
        ("3", "Hard"),
        ("4", "Brutal")
    ]

    title = models.CharField(max_length=75)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.localtime)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    vote_points = models.IntegerField(default=0)
    vote_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    difficulty = models.CharField(default='1', choices=DIFFICULTY_CHOICES, max_length=10)
    ingredients = models.ManyToManyField(Ingredient)
    image = models.ImageField(default='default_recipe.png', upload_to='recipe_images')

    def get_absolute_url(self):
        return reverse('recipe-detail', kwargs={'pk': self.pk})

    def save(self, force_insert=False, force_update=False, using=None):
        super().save()
        image = Image.open(self.image.path)
        image = ImageOps.fit(image, (500, 300), Image.ANTIALIAS)
        image.save(self.image.path)

    def __str__(self):
        return self.title

class Evaluation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    recipce_is_liked = models.BooleanField(default=False)
    recipe_vote = models.IntegerField(default=0, validators=[
        MaxValueValidator(5),
        MinValueValidator(0)
    ])
    date = models.DateTimeField(default=timezone.localtime)

    class Meta:
        unique_together = ("user", "recipe")

    def __str__(self):
        return str(self.user) + ':' + str(self.recipe) + ':Liked=' + str(self.recipce_is_liked) + ':Vote=' + str(self.recipe_vote)