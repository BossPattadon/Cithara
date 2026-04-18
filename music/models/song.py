from django.db import models
from .user import SongCreator
from .library import Library

class Song(models.Model):
    GENRE_CHOICES = [
        ('POP', 'Pop'),
        ('ROCK', 'Rock'),
        ('JAZZ', 'Jazz'),
        ('HIPHOP', 'Hip-hop'),
        ('COUNTRY', 'Country'),
    ]

    MOOD_CHOICES = [
        ('HAPPY', 'Happy'),
        ('SAD', 'Sad'),
        ('ROMANTIC', 'Romantic'),
        ('ENERGETIC', 'Energetic'),
        ('CALM', 'Calm'),
    ]

    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES)
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES)
    occasion = models.CharField(max_length=200)
    prompt_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    audio_file_path = models.CharField(max_length=255)

    creator = models.ForeignKey(SongCreator, on_delete=models.CASCADE)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class ShareLink(models.Model):
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    song = models.ForeignKey(Song, on_delete=models.CASCADE)