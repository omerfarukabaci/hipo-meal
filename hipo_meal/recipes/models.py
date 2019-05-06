from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Recipe(models.Model):
    title = models.CharField(max_length=75)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    vote_points = models.IntegerField()
    vote_count = models.IntegerField()
    like_count = models.IntegerField()
    # Maybe add an image field here.