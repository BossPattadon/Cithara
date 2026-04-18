from django.core.management.base import BaseCommand
from music.generation.generate import get_song_generator
from music.generation.base import GenerationRequest


class Command(BaseCommand):
    help = "Demonstrate the song generation strategy (mock or suno)"

    def add_arguments(self, parser):
        parser.add_argument("--task-id", type=str, help="Check status of an existing task instead of generating new")

    def handle(self, *args, **options):
        generator = get_song_generator()
        self.stdout.write(f"Strategy: {generator.__class__.__name__}\n")

        task_id = options.get("task_id")

        if task_id:
            status_result = generator.get_status(task_id)
            self.stdout.write(f"Task ID : {status_result.task_id}")
            self.stdout.write(f"Status  : {status_result.status}")
            if status_result.audio_url:
                self.stdout.write(f"Audio   : {status_result.audio_url}")
            return

        request = GenerationRequest(
            title="Demo Song",
            genre="POP",
            mood="HAPPY",
            occasion="Birthday Party",
            prompt_text="An upbeat birthday song with cheerful melody",
        )

        result = generator.generate(request)
        self.stdout.write(f"Task ID : {result.task_id}")
        self.stdout.write(f"Status  : {result.status}")
        if result.audio_url:
            self.stdout.write(f"Audio   : {result.audio_url}")

        self.stdout.write(f"\nStatus check : {result.status}")
        if result.audio_url:
            self.stdout.write(f"Audio URL    : {result.audio_url}")
