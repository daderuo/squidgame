from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    total_games = models.IntegerField(default=0)
    win_games =models.IntegerField(default=0)

    def is_valid_user(self):
        return self.total_games >= self.win_games and self.total_games >=0 and self.win_games >= 0

    def serialize(self):
        return {
            "id": self.id,
            "user": self.username,
            "total_games": self.total_games,
            "win_games": self.win_games,
        }

class  Game(models.Model):
    name = models.CharField(max_length=50)
    #single_player = models.BooleanField(default=True)
    #multiplayer = models.BooleanField(default=False)
    img = models.ImageField(upload_to='photo/', default='none')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            #"single_player": self.single_player,
            #"multiplayer": self.multiplayer,
            "photo": str(self.img)
        }
