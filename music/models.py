from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

class SongCreator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Listener(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Library(models.Model):
    owner = models.OneToOneField(SongCreator, on_delete=models.CASCADE)

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
    prompt_text = models.TextField(max_length=1000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    audio_file_path = models.CharField(max_length=255)

    creator = models.ForeignKey(SongCreator, on_delete=models.CASCADE)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

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

class ShareLink(models.Model):
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    song = models.ForeignKey(Song, on_delete=models.CASCADE)