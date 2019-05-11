from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image, ImageOps

class Recipe(models.Model):
    title = models.CharField(max_length=75)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.localtime)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    vote_points = models.IntegerField(default=0)
    vote_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    image = models.ImageField(default='default_recipe.png', upload_to='recipe_images')

    def get_absolute_url(self):
        return reverse('recipe-detail', kwargs={'pk': self.pk})

    def save(self):
        super().save()
        image = Image.open(self.image.path)
        image = ImageOps.fit(image, (500, 300), Image.ANTIALIAS)
        image.save(self.image.path)

    def __str__(self):
        return self.title