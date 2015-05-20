from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Sticker(models.Model):
    number = models.CharField(max_length=10)
    order = models.IntegerField()
    name = models.CharField(max_length=30)
    team = models.CharField(max_length=30)
    image = models.CharField(max_length=300)


class NeededStickers(models.Model):
    user = models.ForeignKey(User)
    sticker = models.ForeignKey(Sticker)


class DuplicatedStickers(models.Model):
    user = models.ForeignKey(User)
    sticker = models.ForeignKey(Sticker)
    quantity = models.IntegerField()