from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class GenerationRequest:
    title: str
    genre: str
    mood: str
    occasion: str
    prompt_text: Optional[str] = None


@dataclass
class GenerationResult:
    task_id: str
    status: str
    audio_url: Optional[str] = None


class SongGeneratorStrategy(ABC):
    @abstractmethod
    def generate(self, request: GenerationRequest) -> GenerationResult:
        pass

    @abstractmethod
    def get_status(self, task_id: str) -> GenerationResult:
        pass
