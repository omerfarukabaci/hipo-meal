from django.db import models
from django.contrib.auth.models import User
from PIL import Image, ImageOps

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default_user_male.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()
        image = Image.open(self.image.path)
        image = ImageOps.fit(image, (150, 150), Image.ANTIALIAS)
        image.save(self.image.path)
