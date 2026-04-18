from django.conf import settings
from .base import SongGeneratorStrategy
from .mock import MockSongGeneratorStrategy
from .suno import SunoSongGeneratorStrategy


def get_song_generator() -> SongGeneratorStrategy:
    strategy = getattr(settings, "GENERATOR_STRATEGY", "mock").lower()
    if strategy == "suno":
        return SunoSongGeneratorStrategy()
    return MockSongGeneratorStrategy()
