# Kling AI SDK Architecture

## Overview

This is a modern, fully-typed Python SDK for the Kling AI API. The SDK is designed with:

- **Clean separation of concerns** - Each API endpoint has its own module
- **Full type safety** - Pydantic v2 models for all requests/responses
- **Async/sync support** - Both synchronous and asynchronous interfaces
- **Auto polling** - Built-in task polling with configurable intervals
- **Smart routing** - Automatically routes single vs multi-image requests

## Directory Structure

```
kling/
├── __init__.py              # Package exports
├── client.py                # Main KlingClient class
├── base.py                  # Base API client with auth & polling
├── exceptions.py            # Custom exceptions
│
├── models/                  # Pydantic models
│   ├── common.py            # Shared models (TaskResponse, VideoResult, etc.)
│   ├── video.py             # Video generation request/response models
│   ├── avatar.py            # Avatar & lip-sync models
│   ├── audio.py             # Audio generation models
│   └── effects.py           # Video effects models
│
└── api/                     # API endpoint implementations
    ├── text_to_video.py     # Text-to-video API
    ├── image_to_video.py    # Image-to-video (single & multi)
    ├── video_extension.py   # Video extension API
    ├── avatar.py            # Avatar generation API
    ├── lip_sync.py          # Lip-sync API
    ├── video_effects.py     # Video effects API
    └── audio.py             # Audio APIs (text2audio, video2audio, TTS)
```

## Core Components

### 1. BaseAPIClient (`base.py`)

The foundation of all API calls. Provides:

- HTTP client management (httpx)
- Authentication (Bearer token)
- Request/response handling
- Error handling
- Polling logic (sync & async)
- Context managers

```python
class BaseAPIClient:
    def post(self, endpoint, json) -> dict
    def get(self, endpoint, params) -> dict
    def wait_for_completion(self, task_id, get_task_func, ...) -> TaskResponse
    # + async versions
```

### 2. KlingClient (`client.py`)

The main entry point. Initializes all API endpoints:

```python
client = KlingClient(api_key="...")

# Access APIs via properties
client.text_to_video
client.image_to_video
client.video_extension
client.avatar
client.lip_sync
client.video_effects
client.text_to_audio
client.video_to_audio
client.tts
```

### 3. API Modules (`api/`)

Each API module follows a consistent pattern:

```python
class SomeAPI:
    def create(**kwargs) -> TaskResponse
    async def create_async(**kwargs) -> TaskResponse

    def get(task_id) -> TaskResponse
    async def get_async(task_id) -> TaskResponse

    def list(page_num, page_size) -> List[TaskResponse]
    async def list_async(...) -> List[TaskResponse]

    def wait_for_completion(task_id, ...) -> TaskResponse
    async def wait_for_completion_async(...) -> TaskResponse
```

### 4. Models (`models/`)

Pydantic v2 models for type safety and validation:

**Common Models** (`common.py`):
- `TaskResponse` - Generic task response
- `VideoResult` - Video output
- `AudioResult` - Audio output
- `CameraControl` - Camera movement configuration

**Request Models**:
- `TextToVideoRequest`
- `ImageToVideoRequest`
- `MultiImageToVideoRequest`
- `VideoExtensionRequest`
- `AvatarRequest`
- `LipSyncRequest`
- etc.

## Key Design Decisions

### 1. Unified Image-to-Video Interface

Instead of separate methods for single and multi-image:

```python
# Single image
client.image_to_video.create(image="url", ...)

# Multi-image (automatically detects)
client.image_to_video.create(images=["url1", "url2"], ...)
```

The SDK automatically routes to:
- `/v1/videos/image2video` (single image)
- `/v1/videos/multi-image2video` (multi-image)

### 2. Consistent Polling Pattern

All async operations use the same polling pattern:

```python
# Create task
task = client.text_to_video.create(...)

# Poll until complete
result = client.text_to_video.wait_for_completion(
    task.task_id,
    poll_interval=5.0,  # seconds between polls
    timeout=600.0       # max wait time
)
```

### 3. Both Sync and Async

Every API call has both sync and async versions:

```python
# Synchronous
task = client.text_to_video.create(...)
result = client.text_to_video.wait_for_completion(task.task_id)

# Asynchronous
task = await client.text_to_video.create_async(...)
result = await client.text_to_video.wait_for_completion_async(task.task_id)
```

### 4. Context Managers

Automatic resource cleanup:

```python
# Sync
with KlingClient(api_key="...") as client:
    task = client.text_to_video.create(...)
# HTTP client automatically closed

# Async
async with KlingClient(api_key="...") as client:
    task = await client.text_to_video.create_async(...)
# HTTP client automatically closed
```

## Model Version Support

The SDK supports all Kling model versions:

| Model | Description | Supports |
|-------|-------------|----------|
| `kling-v1` | Original | Text2Video, Image2Video |
| `kling-v1-5` | Enhanced v1.5 | Text2Video, Image2Video |
| `kling-v1-6` | v1.6 with multi-image | + Multi-Image, Effects |
| `kling-v2-master` | v2.0 | Text2Video, Image2Video |
| `kling-v2-1-master` | v2.1 (recommended) | Text2Video, Image2Video |
| `kling-v2-5-turbo` | Fast v2.5 | Text2Video, Image2Video |

## API Endpoint Mapping

| Feature | SDK Method | API Endpoint |
|---------|------------|--------------|
| Text to Video | `client.text_to_video.create()` | `/v1/videos/text2video` |
| Image to Video | `client.image_to_video.create()` | `/v1/videos/image2video` |
| Multi-Image | `client.image_to_video.create(images=[...])` | `/v1/videos/multi-image2video` |
| Video Extension | `client.video_extension.create()` | `/v1/videos/video-extend` |
| Avatar | `client.avatar.create()` | `/v1/videos/avatar/image2video` |
| Identify Faces | `client.lip_sync.identify_faces()` | `/v1/videos/Identify-face` |
| Lip Sync | `client.lip_sync.create()` | `/v1/videos/advanced-lip-sync` |
| Video Effects | `client.video_effects.create()` | `/v1/videos/effects` |
| Text to Audio | `client.text_to_audio.create()` | `/v1/audio/text-to-audio` |
| Video to Audio | `client.video_to_audio.create()` | `/v1/audio/video-to-audio` |
| TTS | `client.tts.create()` | `/v1/audio/tts` |

## Error Handling

Custom exceptions for different error types:

```python
from kling import KlingAPIError, KlingTimeoutError, KlingValidationError

try:
    task = client.text_to_video.create(...)
except KlingValidationError as e:
    # Request validation failed
    print(f"Validation error: {e}")
except KlingAPIError as e:
    # API returned error
    print(f"API error [{e.code}]: {e.message}")
    print(f"Request ID: {e.request_id}")
except KlingTimeoutError as e:
    # Task didn't complete in time
    print(f"Timeout: {e}")
```

## Extensibility

Adding new endpoints is straightforward:

1. **Create model** in `models/`:
   ```python
   class NewFeatureRequest(BaseModel):
       param1: str
       param2: Optional[int] = None
   ```

2. **Create API class** in `api/`:
   ```python
   class NewFeatureAPI:
       def __init__(self, client: BaseAPIClient):
           self.client = client
           self.endpoint = "/v1/new-feature"

       def create(self, **kwargs) -> TaskResponse:
           request = NewFeatureRequest(**kwargs)
           response = self.client.post(self.endpoint, json=request.model_dump())
           return APIResponse(**response).data
   ```

3. **Add to KlingClient** in `client.py`:
   ```python
   self.new_feature = NewFeatureAPI(self._base_client)
   ```

## Testing

While not included in this initial version, the architecture supports:

- **Unit tests** - Mock httpx responses
- **Integration tests** - Test against real API with test keys
- **Type checking** - mypy for static type analysis

## Future Enhancements

Potential improvements:

1. **Retry logic** - Automatic retries for transient failures
2. **Rate limiting** - Built-in rate limit handling
3. **Caching** - Cache task results
4. **Webhooks** - Handle callback notifications
5. **Streaming** - Stream large file uploads
6. **Batch operations** - Create multiple tasks at once

## Dependencies

Minimal dependencies for maximum compatibility:

- `httpx` (>=0.25.0) - Modern HTTP client with async support
- `pydantic` (>=2.0.0) - Data validation and type hints
- `typing-extensions` (>=4.8.0) - Backport of typing features

Python 3.8+ required.
