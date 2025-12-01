# Kling AI Python SDK - Complete Summary

## What We Built

A fully-typed, production-ready Python SDK for the Kling AI API with comprehensive support for all endpoints.

## Key Features

✅ **Complete API Coverage**
- Text-to-Video (all model versions)
- Image-to-Video (single & multi-image)
- Video Extension
- Avatar Generation
- Lip-Sync
- Video Effects (130+ effects)
- Audio Generation (Text-to-Audio, Video-to-Audio, TTS)

✅ **Modern Architecture**
- Full type safety with Pydantic v2
- Both sync and async interfaces
- Automatic task polling
- Smart routing (single vs multi-image)
- Context managers for resource cleanup

✅ **Developer Experience**
- Clean, intuitive API
- Comprehensive examples
- Detailed documentation
- Proper error handling

## Installation

```bash
pip install -e .
```

## Quick Start

```python
from kling import KlingClient

# Initialize with Access Key and Secret Key
client = KlingClient(
    access_key="ak-your-access-key",
    secret_key="your-secret-key"
)

# Generate a video
task = client.text_to_video.create(
    model_name="kling-v2-1-master",
    prompt="A cat playing piano",
    duration="5"
)

# Wait for completion
result = client.text_to_video.wait_for_completion(task.task_id)
print(f"Video: {result.task_result.videos[0].url}")
```

## Project Structure

```
kling/
├── kling/
│   ├── __init__.py           # Package exports
│   ├── client.py             # Main KlingClient
│   ├── base.py               # Base API client with auth & polling
│   ├── exceptions.py         # Custom exceptions
│   ├── models/               # Pydantic models
│   │   ├── common.py         # Shared models
│   │   ├── video.py          # Video models
│   │   ├── avatar.py         # Avatar & lip-sync models
│   │   ├── audio.py          # Audio models
│   │   └── effects.py        # Effects models
│   └── api/                  # API implementations
│       ├── text_to_video.py
│       ├── image_to_video.py
│       ├── video_extension.py
│       ├── avatar.py
│       ├── lip_sync.py
│       ├── video_effects.py
│       └── audio.py
├── examples/
│   ├── basic_usage.py
│   ├── async_usage.py
│   └── advanced_features.py
├── README.md
├── QUICKSTART.md
├── AUTHENTICATION.md
├── ARCHITECTURE.md
├── CONTRIBUTING.md
└── pyproject.toml
```

## Authentication

Kling AI uses Access Key and Secret Key authentication:

```python
import os
from kling import KlingClient

client = KlingClient(
    access_key=os.getenv("KLING_ACCESS_KEY"),
    secret_key=os.getenv("KLING_SECRET_KEY")
)
```

Set environment variables:

```bash
export KLING_ACCESS_KEY="ak-your-access-key"
export KLING_SECRET_KEY="your-secret-key"
```

## Core APIs

### Video Generation

```python
# Text to Video
task = client.text_to_video.create(
    model_name="kling-v2-1-master",
    prompt="A sunset over mountains",
    duration="5",
    mode="pro"
)

# Image to Video (single)
task = client.image_to_video.create(
    image="https://example.com/image.jpg",
    prompt="The person walks forward"
)

# Multi-Image to Video
task = client.image_to_video.create(
    images=["img1.jpg", "img2.jpg"],
    prompt="Two people meeting"
)

# Video Extension
task = client.video_extension.create(
    video_id="video-id",
    prompt="Continue the scene"
)
```

### Avatar & Lip-Sync

```python
# Avatar
task = client.avatar.create(
    image="face.jpg",
    audio_id="audio-id",
    prompt="Speaking with emotion"
)

# Lip-Sync
faces = client.lip_sync.identify_faces(video_id="video-id")
task = client.lip_sync.create(
    session_id=faces.session_id,
    face_choose=[{
        "face_id": faces.face_data[0].face_id,
        "audio_id": "audio-id",
        "sound_start_time": 0,
        "sound_end_time": 5000,
        "sound_insert_time": 0
    }]
)
```

### Audio

```python
# Text to Audio
task = client.text_to_audio.create(
    prompt="Ocean waves",
    duration=5.0
)

# TTS
result = client.tts.create(
    text="Hello world",
    voice_id="voice_001",
    voice_language="en"
)

# Video to Audio
task = client.video_to_audio.create(
    video_id="video-id",
    sound_effect_prompt="Nature sounds",
    bgm_prompt="Ambient music"
)
```

### Video Effects

```python
# Single image effect
task = client.video_effects.create(
    effect_scene="pet_lion",
    input={"image": "cat.jpg", "duration": "5"}
)

# Dual character effect
task = client.video_effects.create(
    effect_scene="hug",
    input={
        "model_name": "kling-v1-6",
        "images": ["person1.jpg", "person2.jpg"],
        "duration": "5"
    }
)
```

## Advanced Features

### Camera Control

```python
task = client.text_to_video.create(
    prompt="Mountain landscape",
    camera_control={
        "type": "simple",
        "config": {"zoom": -5}  # Zoom in
    }
)
```

### Motion Brush (Dynamic Masks)

```python
task = client.image_to_video.create(
    image="scene.jpg",
    dynamic_masks=[{
        "mask": "mask.png",
        "trajectories": [
            {"x": 100, "y": 200},
            {"x": 300, "y": 200}
        ]
    }]
)
```

### Async Support

```python
import asyncio

async def main():
    client = KlingClient(access_key="...", secret_key="...")
    
    task = await client.text_to_video.create_async(prompt="...")
    result = await client.text_to_video.wait_for_completion_async(task.task_id)
    print(result.task_result.videos[0].url)

asyncio.run(main())
```

## Supported Models

- `kling-v1` - Original
- `kling-v1-5` - Enhanced
- `kling-v1-6` - Multi-image support
- `kling-v2-master` - V2.0
- `kling-v2-1-master` - V2.1 (recommended)
- `kling-v2-5-turbo` - Fast V2.5

## Error Handling

```python
from kling import KlingAPIError, KlingTimeoutError, KlingValidationError

try:
    task = client.text_to_video.create(...)
    result = client.text_to_video.wait_for_completion(task.task_id)
except KlingValidationError as e:
    print(f"Validation error: {e}")
except KlingAPIError as e:
    print(f"API error [{e.code}]: {e.message}")
except KlingTimeoutError as e:
    print(f"Timeout: {e}")
```

## Documentation

- **README.md** - Overview and features
- **QUICKSTART.md** - Quick start guide with all APIs
- **AUTHENTICATION.md** - Authentication guide
- **ARCHITECTURE.md** - Technical architecture
- **CONTRIBUTING.md** - Development guide
- **examples/** - Working code examples

## Next Steps

1. **Install dependencies**: `pip install -e .`
2. **Set up authentication**: Export your keys
3. **Run examples**: `python examples/basic_usage.py`
4. **Read the docs**: Check QUICKSTART.md
5. **Build something amazing!**

## Dependencies

- `httpx` (>=0.25.0) - HTTP client
- `pydantic` (>=2.0.0) - Data validation
- `typing-extensions` (>=4.8.0) - Type hints

Python 3.8+ required.

## License

MIT License - See LICENSE file
