import uuid
from django.db import models
from .song_creator import SongCreator
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

    share_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    creator = models.ForeignKey(SongCreator, on_delete=models.CASCADE)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
