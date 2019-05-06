from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Recipe(models.Model):
    title = models.CharField(max_length=75)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.localtime)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    vote_points = models.IntegerField(default=0)
    vote_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    # Maybe add an image field here.

    def __str__(self):
        return self.title