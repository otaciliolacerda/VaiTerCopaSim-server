# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DuplicatedStickers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='NeededStickers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sticker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(max_length=10)),
                ('order', models.IntegerField()),
                ('name', models.CharField(max_length=30)),
                ('team', models.CharField(max_length=30)),
                ('image', models.CharField(max_length=300)),
            ],
        ),
        migrations.AddField(
            model_name='neededstickers',
            name='sticker',
            field=models.ForeignKey(to='stickerAPI.Sticker'),
        ),
        migrations.AddField(
            model_name='neededstickers',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='duplicatedstickers',
            name='sticker',
            field=models.ForeignKey(to='stickerAPI.Sticker'),
        ),
        migrations.AddField(
            model_name='duplicatedstickers',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
