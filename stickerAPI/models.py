# -*- coding: utf-8 -*-

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

    def __str__(self):
        return "Number: " + str(self.number)


class NeededStickers(models.Model):
    user = models.ForeignKey(User)
    sticker = models.ForeignKey(Sticker)

    def dict(self):
        return {"user": self.user.id, "sticker": self.sticker.dict()}

    @staticmethod
    def calculate_stats(user_id):
        missing = NeededStickers.objects.filter(user__id=user_id).order_by('sticker__order')

        stats = {'collected': 649 - missing.count(), 'missing': missing.count(), 'teams': {}}

        teams = ['Especiais', 'Estádios', 'Brasil', 'Croácia', 'México', 'Camarões', 'Espanha', 'Holanda', 'Chile',
                 'Austrália', 'Colômbia', 'Grécia', 'Costa do Marfim', 'Japão', 'Uruguai', 'Costa Rica',
                 'Inglaterra', 'Itália', 'Suiça', 'Equador', 'França', 'Honduras', 'Argentina' ,
                 'Bósnia Herzegovina', 'Irã', 'Nigéria', 'Alemanha', 'Portugal', 'Gana', 'Estados Unidos',
                 'Bélgica', 'Algéria', 'Rússia', 'Coréia', 'Propaganda']

        for team in teams:
            stats['teams'][team] = len([i for i in missing if i.sticker.team == team])

        return stats

    def __str__(self):
        return "Number: " + str(self.sticker.number) + " - Owner: " + str(self.user.email)


class DuplicatedStickers(models.Model):
    user = models.ForeignKey(User)
    sticker = models.ForeignKey(Sticker)
    quantity = models.IntegerField()

    def dict(self):
        return {"user": self.user.id, "sticker": self.sticker.dict(), "quantity": self.quantity}

    def __str__(self):
        return "Number/Quantity: " + str(self.sticker.number) + "/" + str(self.quantity) + " - Owner: " + str(self.user.email)