# Sequence Diagram – Song Generation Use Case

This diagram shows the end-to-end flow when a user generates a song, from form submission through to playback.

## Flow Overview

1. **Form submission** — The user fills in the create form and submits. The view creates a `Song` and `SongGeneration` record, then delegates to `SongGeneratorStrategy`.
2. **Strategy dispatch** — In **Suno mode**, the strategy calls the Suno API and receives a `taskId`. The generation status is set to `PROCESSING`. In **Mock mode**, the result is returned immediately and status is set to `COMPLETED`.
3. **Status polling** — The browser is redirected to the status page. A JavaScript `setInterval` polls `/song/{id}/status/api/` every 5 seconds. Each poll triggers a server-side check against the Suno API.
4. **Completion** — Once Suno returns `SUCCESS`, the `SongGeneration` status is updated to `COMPLETED` and the audio URL is saved. The browser reloads and renders the completed state.

```mermaid
sequenceDiagram
    actor User
    participant Browser
    participant Views
    participant SongGeneratorStrategy
    participant SunoAPI
    participant DB

    User->>Browser: Fill form and submit
    Browser->>Views: POST /generate/

    Views->>DB: Create Song (PENDING)
    Views->>DB: Create SongGeneration (PENDING)
    Views->>SongGeneratorStrategy: generate(GenerationRequest)

    alt Suno mode
        SongGeneratorStrategy->>SunoAPI: POST /generate (prompt, style, title)
        SunoAPI-->>SongGeneratorStrategy: { taskId: "abc123" }
        SongGeneratorStrategy-->>Views: GenerationResult(task_id, PENDING)
        Views->>DB: Update SongGeneration → PROCESSING, task_id="abc123"
    else Mock mode
        SongGeneratorStrategy-->>Views: GenerationResult(task_id, SUCCESS, audio_url)
        Views->>DB: Update SongGeneration → COMPLETED
        Views->>DB: Update Song.audio_file_path
    end

    Views-->>Browser: Redirect to /song/{id}/status/
    Browser->>Views: GET /song/{id}/status/
    Views->>SunoAPI: get_status(task_id)
    SunoAPI-->>Views: { status: PENDING }
    Views-->>Browser: Render status.html (PROCESSING)

    loop Poll every 5 seconds
        Browser->>Views: GET /song/{id}/status/api/
        Views->>SunoAPI: get_status(task_id)
        SunoAPI-->>Views: { status, audio_url }

        alt status == SUCCESS
            Views->>DB: Update SongGeneration → COMPLETED
            Views->>DB: Update Song.audio_file_path
            Views-->>Browser: { status: COMPLETED }
            Browser->>Browser: location.reload()
            Browser->>Views: GET /song/{id}/status/
            Views-->>Browser: Render status.html (COMPLETED)
        else status == FAILED / ERROR
            Views->>DB: Update SongGeneration → FAILED
            Views-->>Browser: { status: FAILED }
            Browser->>Browser: location.reload()
        else still PENDING / PROCESSING
            Views-->>Browser: { status: PROCESSING }
        end
    end
```
