from django.db import models

class Leaderboard(models.Model):
    score = models.IntegerField(default=0)
    username = models.TextField(default="Anonymous")
    date = models.DateField()
