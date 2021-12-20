from django.contrib.auth.models import AbstractUser
from django.db import models
from random import *

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



class Match(models.Model):
    opp1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="opponent1")
    opp2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="opponent2")
    turn = models.IntegerField(default=random())
    opp1_ball = models.IntegerField(default=10)
    opp1_ball_sel = models.IntegerField(default=0)
    opp1_ball_guess = models.BooleanField(default=False)
    opp2_ball = models.IntegerField(default=10)
    opp2_ball_sel = models.IntegerField(default=0)
    opp2_ball_guess = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="match_winner")

    def is_valid_Match(self):
        return self.opp1 != self.opp2 

    def serialize(self):
        return {
            "opp1": self.opp1.username,
            "opp2": self.opp2.username,
            "turn": self.turn,
            "opp1_ball": self.opp1_ball,
            "opp2_ball": self.opp2_ball,
            "opp1_ball_sel": self.opp1_ball_sel,
            "opp2_ball_sel": self.opp2_ball_sel,
            "opp1_ball_guess": self.opp1_ball_guess,
            "opp2_ball_guess": self.opp2_ball_guess,
            "active": self.active,
            "game": self.game.name,
            "winner": self.winner.username,
        }

class Wait(models.Model):
    opp = models.ForeignKey(User, on_delete=models.CASCADE, related_name="opp")
    game = models.ForeignKey(Game, on_delete=models.CASCADE)