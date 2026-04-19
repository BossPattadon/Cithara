import re
import requests as http_requests
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, StreamingHttpResponse
from django.contrib.auth.decorators import login_required

from music.models import Song, SongGeneration, SongCreator, Library, ShareLink
from music.generation.generate import get_song_generator
from music.generation.base import GenerationRequest


def _get_creator(auth_user):
    creator, _ = SongCreator.objects.get_or_create(
        email=auth_user.email,
        defaults={'name': auth_user.get_full_name() or auth_user.username},
    )
    library, _ = Library.objects.get_or_create(owner=creator)
    return creator, library


def _refresh_status(song, generation):
    if generation.status not in ('PENDING', 'PROCESSING') or not generation.task_id:
        return
    try:
        result = get_song_generator().get_status(generation.task_id)
        if result.status == 'SUCCESS':
            generation.status = 'COMPLETED'
            if result.audio_url:
                song.audio_file_path = result.audio_url
                song.save()
        elif result.status in ('FAILED', 'ERROR'):
            generation.status = 'FAILED'
        generation.save()
    except Exception:
        pass


def index(request):
    return render(request, 'music/index.html')


@login_required
def create_song(request):
    return render(request, 'music/create.html', {
        'genre_choices': Song.GENRE_CHOICES,
        'mood_choices': Song.MOOD_CHOICES,
    })


@login_required
def generate_song(request):
    if request.method != 'POST':
        return redirect('create_song')

    title = request.POST.get('title', '').strip()
    genre = request.POST.get('genre', '')
    mood = request.POST.get('mood', '')
    occasion = request.POST.get('occasion', '').strip()
    prompt_text = request.POST.get('prompt_text', '').strip()

    creator, library = _get_creator(request.user)
    song = Song.objects.create(
        title=title,
        genre=genre,
        mood=mood,
        occasion=occasion,
        prompt_text=prompt_text,
        audio_file_path='',
        creator=creator,
        library=library,
    )
    generation = SongGeneration.objects.create(song=song, status='PENDING')

    try:
        generator = get_song_generator()
        result = generator.generate(GenerationRequest(
            title=title,
            genre=genre,
            mood=mood,
            occasion=occasion,
            prompt_text=prompt_text or None,
        ))
        generation.task_id = result.task_id
        if result.audio_url:
            song.audio_file_path = result.audio_url
            song.save()
            generation.status = 'COMPLETED'
        else:
            generation.status = 'PROCESSING'
        generation.save()
    except Exception:
        generation.status = 'FAILED'
        generation.save()

    return redirect('song_status', song_id=song.id)


@login_required
def song_status(request, song_id):
    creator, _ = _get_creator(request.user)
    song = get_object_or_404(Song, id=song_id, creator=creator)
    generation = get_object_or_404(SongGeneration, song=song)
    _refresh_status(song, generation)
    return render(request, 'music/status.html', {'song': song, 'generation': generation})


def check_status_api(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    generation = get_object_or_404(SongGeneration, song=song)
    _refresh_status(song, generation)
    return JsonResponse({
        'status': generation.status,
        'audio_url': song.audio_file_path or None,
    })


@login_required
def library(request):
    creator, _ = _get_creator(request.user)
    songs = Song.objects.filter(creator=creator).select_related('songgeneration').order_by('-created_at')
    return render(request, 'music/library.html', {'songs': songs})


def song_detail(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    generation = SongGeneration.objects.filter(song=song).first()
    share_links = ShareLink.objects.filter(song=song)
    return render(request, 'music/detail.html', {
        'song': song,
        'generation': generation,
        'share_links': share_links,
    })


@login_required
def delete_song(request, song_id):
    if request.method == 'POST':
        creator, _ = _get_creator(request.user)
        get_object_or_404(Song, id=song_id, creator=creator).delete()
    return redirect('library')


def download_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    r = http_requests.get(song.audio_file_path, stream=True)
    safe_title = re.sub(r'[\\/:*?"<>|]', '', song.title) or 'song'
    response = StreamingHttpResponse(
        r.iter_content(chunk_size=8192),
        content_type='audio/mpeg',
    )
    response['Content-Disposition'] = f'attachment; filename="{safe_title}.mp3"'
    return response


@login_required
def create_share_link(request, song_id):
    if request.method == 'POST':
        song = get_object_or_404(Song, id=song_id)
        share_url = request.build_absolute_uri(f'/song/{song_id}/')
        ShareLink.objects.create(song=song, url=share_url)
    return redirect('song_detail', song_id=song_id)
