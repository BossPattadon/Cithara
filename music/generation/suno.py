import requests
from django.conf import settings
from .base import SongGeneratorStrategy, GenerationRequest, GenerationResult

SUNO_BASE_URL = "https://api.sunoapi.org/api/v1"


class SunoSongGeneratorStrategy(SongGeneratorStrategy):
    def __init__(self):
        self.api_key = settings.SUNO_API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def generate(self, request: GenerationRequest) -> GenerationResult:
        prompt = request.prompt_text or (
            f"A {request.mood.lower()} {request.genre.lower()} song for {request.occasion}"
        )
        # Suno API rejects prompts longer than 500 characters
        prompt = prompt[:500]
        payload = {
            "prompt": prompt,
            "title": request.title,
            "style": f"{request.genre} {request.mood}",
            "customMode": False,
            "instrumental": False,
            "callBackUrl": "https://example.com/callback",
            "model": "V4",
        }
        response = requests.post(
            f"{SUNO_BASE_URL}/generate",
            json=payload,
            headers=self.headers,
        )
        response.raise_for_status()
        data = response.json()
        inner = data.get("data") or {}
        task_id = inner.get("taskId") or data.get("taskId")
        print(f"[Suno] Task created: {task_id}")
        return GenerationResult(task_id=task_id, status="PENDING")

    def get_status(self, task_id: str) -> GenerationResult:
        response = requests.get(
            f"{SUNO_BASE_URL}/generate/record-info",
            params={"taskId": task_id},
            headers=self.headers,
        )
        response.raise_for_status()
        data = response.json()

        record = data.get("data") or {}
        status = record.get("status", "PENDING")

        audio_url = None
        suno_data = (record.get("response") or {}).get("sunoData") or []
        if suno_data:
            audio_url = suno_data[0].get("audioUrl")

        print(f"[Suno] Task {task_id} status: {status}")
        return GenerationResult(task_id=task_id, status=status, audio_url=audio_url)
