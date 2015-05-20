from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Sticker(models.Model):
    number = models.CharField(max_length=10)
    order = models.IntegerField()
    name = models.CharField(max_length=30)
    team = models.CharField(max_length=30)
    image = models.CharField(max_length=300)

    def dict(self):
        return {"number": self.number, "order": self.order, "name": self.name, "team": self.team, "image": self.image}


class NeededStickers(models.Model):
    user = models.ForeignKey(User)
    sticker = models.ForeignKey(Sticker)

    def dict(self):
        return {"user": self.user.id, "sticker": self.sticker.id}


class DuplicatedStickers(models.Model):
    user = models.ForeignKey(User)
    sticker = models.ForeignKey(Sticker)
    quantity = models.IntegerField()

    def dict(self):
        return {"user": self.user.id, "sticker": self.sticker.id, "quantity": self.quantity}