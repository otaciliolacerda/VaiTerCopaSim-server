from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


# Create your models here.
class Sticker(models.Model):
    number = models.CharField(max_length=10)
    order = models.IntegerField()
    name = models.CharField(max_length=30)
    team = models.CharField(max_length=30)
    image = models.CharField(max_length=300)

    def dict(self):
        return {"number": self.number, "order": self.order, "name": self.name, "team": self.team,
                "image": '%s%s' % (settings.STICKER_IMG_PREFIX, self.image)}

    def __str__(self):
        return "Number: %s" % str(self.number)


class NeededStickers(models.Model):
    user = models.ForeignKey(User)
    sticker = models.ForeignKey(Sticker)

    def dict(self):
        return self.sticker.dict()

    def __str__(self):
        return "Number: %s - Owner: %s" % (self.sticker.number, str(self.user.email))


class DuplicatedStickers(models.Model):
    user = models.ForeignKey(User)
    sticker = models.ForeignKey(Sticker)
    quantity = models.IntegerField()

    def dict(self):
        result = self.sticker.dict()
        result['quantity'] = self.quantity
        return result

    def __str__(self):
        return "Number/Quantity: %s/%s - Owner: %s" % (self.sticker.number, str(self.quantity), self.user.email)