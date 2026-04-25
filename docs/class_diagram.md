# Class Diagram

This diagram shows the full class structure of Cithara following the **Model-View-Template (MVT)** architecture pattern, along with the **Strategy Pattern** used for song generation.

## Layers

- **Model Layer** — Django ORM classes representing the domain entities. `User` is the base class inherited by `SongCreator` and `Listener`. `Song` is the central entity linked to `Library`, `SongGeneration`, and `ShareLink`.
- **View Layer** — Django view functions that handle HTTP requests, interact with models, and trigger song generation.
- **Template Layer** — HTML templates rendered by the views and served to the browser.
- **Strategy Pattern** — `SongGeneratorStrategy` defines the abstract interface for song generation. `MockSongGeneratorStrategy` is used for offline testing; `SunoSongGeneratorStrategy` calls the real Suno API.

```mermaid
classDiagram
    direction LR

    %% ── Model Layer ──────────────────────────────────────────────────────────
    class User {
        <<Model>>
        +name : CharField
        +email : EmailField
        +__str__() str
    }
    class SongCreator {
        <<Model>>
    }
    class Listener {
        <<Model>>
    }
    class Library {
        <<Model>>
        +owner : SongCreator
    }
    class Song {
        <<Model>>
        +title : CharField
        +genre : CharField
        +mood : CharField
        +occasion : CharField
        +prompt_text : TextField
        +audio_file_path : CharField
        +share_token : UUIDField
        +created_at : DateTimeField
        +__str__() str
    }
    class SongGeneration {
        <<Model>>
        +status : CharField
        +task_id : CharField
        +requested_at : DateTimeField
    }
    class ShareLink {
        <<Model>>
        +url : URLField
        +created_at : DateTimeField
    }

    %% ── View Layer ───────────────────────────────────────────────────────────
    class Views {
        <<View>>
        +index()
        +create_song()
        +generate_song()
        +song_status()
        +library()
        +song_detail()
        +delete_song()
        +download_song()
        +shared_song()
        +check_status_api()
    }

    %% ── Template Layer ───────────────────────────────────────────────────────
    class Templates {
        <<Template>>
        base.html
        index.html
        create.html
        status.html
        library.html
        detail.html
        login.html
    }

    %% ── Strategy Pattern ─────────────────────────────────────────────────────
    class SongGeneratorStrategy {
        <<abstract>>
        +generate(request) GenerationResult*
        +get_status(task_id) GenerationResult*
    }
    class MockSongGeneratorStrategy {
        +generate(request) GenerationResult
        +get_status(task_id) GenerationResult
    }
    class SunoSongGeneratorStrategy {
        -api_key : str
        +generate(request) GenerationResult
        +get_status(task_id) GenerationResult
    }
    class GenerationRequest {
        <<dataclass>>
        +title : str
        +genre : str
        +mood : str
        +occasion : str
        +prompt_text : str
    }
    class GenerationResult {
        <<dataclass>>
        +task_id : str
        +status : str
        +audio_url : str
    }

    %% ── Model Relationships ──────────────────────────────────────────────────
    User <|-- SongCreator : inherits
    User <|-- Listener : inherits
    SongCreator "1" --> "1" Library : owns
    SongCreator "1" --> "0..*" Song : creates
    Library "1" --> "0..*" Song : contains
    Song "1" --> "1" SongGeneration : has
    Song "1" --> "0..*" ShareLink : has

    %% ── MVT Relationships ────────────────────────────────────────────────────
    Views --> Song : uses
    Views --> SongGeneration : uses
    Views --> SongGeneratorStrategy : uses
    Views ..> Templates : renders

    %% ── Strategy Relationships ───────────────────────────────────────────────
    SongGeneratorStrategy <|-- MockSongGeneratorStrategy : implements
    SongGeneratorStrategy <|-- SunoSongGeneratorStrategy : implements
    SongGeneratorStrategy ..> GenerationRequest : accepts
    SongGeneratorStrategy ..> GenerationResult : returns
```
