from django.db import models
from .song_creator import SongCreator


class Library(models.Model):
    owner = models.OneToOneField(SongCreator, on_delete=models.CASCADE)
