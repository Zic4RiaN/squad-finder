from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. Modelo CustomUser
class CustomUser(AbstractUser):
    gamertag = models.CharField(max_length=100, unique=True) #

    def __str__(self):
        return f"{self.username} ({self.gamertag})"

# 2. Modelo Game (Catálogo)
class Game(models.Model):
    nombre = models.CharField(max_length=100) #
    slug = models.SlugField(unique=True) #
    cover_image = models.URLField(null=True, blank=True) #

    def __str__(self):
        return self.nombre

# 3. Modelo SquadRequest (La publicación)
class SquadRequest(models.Model):
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='squads') #
    game = models.ForeignKey(Game, on_delete=models.CASCADE) #
    rank_required = models.CharField(max_length=50) #
    mic_required = models.BooleanField(default=False) #
    description = models.TextField() #
    created_at = models.DateTimeField(auto_now_add=True) #