# -*- coding: utf-8 -*-
__author__ = 'otacilio'

from django.db.models import Q
from models import *


def set_team(starting_sticker, ending_sticker, team):
    for s in Sticker.objects.filter(Q(order__gte=starting_sticker) & Q(order__lte=ending_sticker)):
        s.team = team
        s.save()


def add_normal_stickers(starting_order_number, ending_order_number, order_offset=0):
    for i in range(starting_order_number, ending_order_number + 1):
        sticker = Sticker(number=i, order=i + order_offset, image=str(i) + ".jpg")
        sticker.save()


def seed():
    # First, special sticker
    sticker = Sticker(number="00", order=0, image="00.jpg", team="Especiais")
    sticker.save()

    # First batch of regularly numbered stickers
    add_normal_stickers(1, 183)

    # Promotional stickers ('happy family' lol), L1 - L4
    for i in range(184, 187+1):
        number = "L" + str(4-(187-i))
        sticker = Sticker(number=number, order=i, image=number+".jpg")
        sticker.save()

    # Second batch of regularly numbered stickers
    add_normal_stickers(184,335,4)

    # Promotional sticker (wise up)
    sticker = Sticker(number="W1", order=340, image="W1.jpg")
    sticker.save()

    # Third and last batch..
    add_normal_stickers(336,639,5)

    # Last promotional stickers (Fuleco), J1 - J4
    for i in range(645, 648+1):
        number = "J" + str(4-(648-i))
        sticker = Sticker(number=number, order=i, image=number+".jpg")
        sticker.save()


    set_team(1,7,"Especiais")
    set_team(8,31,"Estádios")
    set_team(32,50,"Brasil")
    set_team(51,69,"Croácia")
    set_team(70,88,"México")
    set_team(89,107,"Camarões")
    set_team(108,126,"Espanha")
    set_team(127,145,"Holanda")
    set_team(146,164,"Chile")
    set_team(165,183,"Austrália")

    set_team(184,187,"Propaganda")

    set_team(188,206,"Colômbia")
    set_team(207,225,"Grécia")
    set_team(226,244,"Costa do Marfim")
    set_team(245,263,"Japão")
    set_team(264,282,"Uruguai")
    set_team(283,301,"Costa Rica")
    set_team(302,320,"Inglaterra")
    set_team(321,339,"Itália")

    set_team(340,340,"Propaganda")

    set_team(341,359,"Suiça")
    set_team(360,378,"Equador")
    set_team(379,397,"França")
    set_team(398,416,"Honduras")
    set_team(417,435,"Argentina")
    set_team(436,454,"Bósnia Herzegovina")
    set_team(455,473,"Irã")
    set_team(474,492,"Nigéria")
    set_team(493,511,"Alemanha")
    set_team(512,530,"Portugal")
    set_team(531,549,"Gana")
    set_team(550,568,"Estados Unidos")
    set_team(569,587,"Bélgica")
    set_team(588,606,"Algéria")
    set_team(607,625,"Rússia")
    set_team(626,644,"Coréia")

    set_team(645,648,"Propaganda")