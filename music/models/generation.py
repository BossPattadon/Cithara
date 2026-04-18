from django.db import models
from .song import Song

class SongGeneration(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    task_id = models.CharField(max_length=200, blank=True, null=True)
    requested_at = models.DateTimeField(auto_now_add=True)

    song = models.OneToOneField(Song, on_delete=models.CASCADE)