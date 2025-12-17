from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    gamertag = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.gamertag

class Game(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    cover_image = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class SquadRequest(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='squads'
    )
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name='squads'
    )
    rank_required = models.CharField(max_length=30)
    mic_required = models.BooleanField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.game.name} - {self.user.gamertag}"

