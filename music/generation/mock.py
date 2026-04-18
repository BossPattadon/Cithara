import uuid
from .base import SongGeneratorStrategy, GenerationRequest, GenerationResult


class MockSongGeneratorStrategy(SongGeneratorStrategy):
    def generate(self, request: GenerationRequest) -> GenerationResult:
        task_id = f"mock-{uuid.uuid4().hex[:8]}"
        print(f"[Mock] Generating song: '{request.title}' | genre={request.genre} mood={request.mood}")
        return GenerationResult(
            task_id=task_id,
            status="SUCCESS",
            audio_url="https://example.com/mock-audio.mp3",
        )

    def get_status(self, task_id: str) -> GenerationResult:
        print(f"[Mock] Checking status for task: {task_id}")
        return GenerationResult(
            task_id=task_id,
            status="SUCCESS",
            audio_url="https://example.com/mock-audio.mp3",
        )
