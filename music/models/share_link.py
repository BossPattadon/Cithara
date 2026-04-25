from django.db import models
from .song import Song


class ShareLink(models.Model):
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    song = models.ForeignKey(Song, on_delete=models.CASCADE)
