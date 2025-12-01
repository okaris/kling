# Kling AI Python SDK

A modern, fully-typed Python SDK for the Kling AI API. Generate videos from text and images, create avatars, apply effects, and more.

## Features

- 🎯 **Fully Typed** - Complete type hints with Pydantic v2 models
- 🔄 **Auto Polling** - Automatic task polling with customizable intervals
- 🎨 **Model Versions** - Support for all Kling model versions (v1, v1-5, v1-6, v2, v2-1, v2-5-turbo)
- 🎬 **Video Generation** - Text-to-video, image-to-video, multi-image, and video extension
- 👤 **Avatar & Effects** - Avatar generation, lip-sync, and 130+ video effects
- 🎵 **Audio** - Text-to-audio, video-to-audio, and TTS
- 📦 **Modular Design** - Clean separation by feature and model version
- ⚡ **Async/Sync** - Both async and sync interfaces

## Installation

```bash
# Using Poetry (recommended)
poetry add kling-sdk

# Using pip
pip install kling-sdk
```

## Quick Start

```python
from kling import KlingClient

# Initialize the client
client = KlingClient(api_key="your-api-key")

# Generate a video from text
task = client.text_to_video.create(
    model_name="kling-v2-1-master",
    prompt="A beautiful sunset over mountains",
    duration="5",
    mode="pro"
)

# Wait for completion
result = client.text_to_video.wait_for_completion(task.task_id)
print(f"Video URL: {result.task_result.videos[0].url}")
```

## Async Usage

```python
import asyncio
from kling import KlingClient

async def main():
    client = KlingClient(api_key="your-api-key")

    # Generate video asynchronously
    task = await client.text_to_video.create_async(
        model_name="kling-v2-1-master",
        prompt="A beautiful sunset over mountains",
        duration="5"
    )

    # Wait for completion
    result = await client.text_to_video.wait_for_completion_async(task.task_id)
    print(f"Video URL: {result.task_result.videos[0].url}")

asyncio.run(main())
```

## API Overview

### Video Generation

```python
# Text to Video
task = client.text_to_video.create(
    model_name="kling-v2-1-master",
    prompt="A cat playing piano",
    duration="5",
    mode="pro"
)

# Image to Video (single image)
task = client.image_to_video.create(
    model_name="kling-v1-6",
    image="https://example.com/image.jpg",
    prompt="The person starts walking"
)

# Image to Video (multi-image)
task = client.image_to_video.create(
    model_name="kling-v1-6",
    images=[
        {"image": "https://example.com/img1.jpg"},
        {"image": "https://example.com/img2.jpg"}
    ],
    prompt="Combine these characters"
)

# Video Extension
task = client.video_extension.create(
    video_id="existing-video-id",
    prompt="Continue the scene"
)
```

### Avatar & Effects

```python
# Avatar generation
task = client.avatar.create(
    image="https://example.com/face.jpg",
    audio_id="tts-audio-id",
    prompt="Speaking with emotion"
)

# Lip Sync
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

# Video Effects
task = client.video_effects.create(
    effect_scene="pet_lion",
    input={"image": "https://example.com/img.jpg", "duration": "5"}
)
```

### Audio

```python
# Text to Audio
task = client.text_to_audio.create(
    prompt="Ocean waves and birds chirping",
    duration=5.0
)

# TTS
task = client.tts.create(
    text="Hello, welcome to Kling AI!",
    voice_id="voice_001",
    voice_language="en"
)

# Video to Audio
task = client.video_to_audio.create(
    video_id="video-id",
    sound_effect_prompt="Add nature sounds",
    bgm_prompt="Calm ambient music"
)
```

## Directory Structure

```
kling/
├── __init__.py
├── client.py              # Main client
├── base.py                # Base API client with auth & polling
├── models/                # Pydantic models
│   ├── __init__.py
│   ├── common.py          # Common models (TaskResponse, VideoResult, etc.)
│   ├── video.py           # Video generation models
│   ├── avatar.py          # Avatar models
│   ├── audio.py           # Audio models
│   └── effects.py         # Effects models
├── api/                   # API endpoints
│   ├── __init__.py
│   ├── text_to_video.py
│   ├── image_to_video.py
│   ├── video_extension.py
│   ├── avatar.py
│   ├── lip_sync.py
│   ├── video_effects.py
│   ├── text_to_audio.py
│   ├── video_to_audio.py
│   └── tts.py
└── exceptions.py          # Custom exceptions
```

## License

MIT
