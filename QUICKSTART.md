# Kling AI SDK - Quick Start Guide

## Installation

```bash
# Install with pip
pip install -e .

# Or with poetry
poetry install
```

## Basic Usage

```python
from kling import KlingClient

# Initialize client
client = KlingClient(api_key="your-api-key")

# Generate video from text
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

## Supported Models

- **kling-v1** - Original model
- **kling-v1-5** - Enhanced version 1.5
- **kling-v1-6** - Version 1.6 with multi-image support
- **kling-v2-master** - Version 2.0
- **kling-v2-1-master** - Version 2.1 (recommended)
- **kling-v2-5-turbo** - Fast version 2.5

## Key Features

### 1. Text to Video

```python
task = client.text_to_video.create(
    model_name="kling-v2-1-master",
    prompt="Your text prompt here",
    duration="5",  # "5" or "10" seconds
    mode="std",    # "std" or "pro"
    aspect_ratio="16:9"  # "16:9", "9:16", or "1:1"
)
```

### 2. Image to Video (Single Image)

```python
task = client.image_to_video.create(
    model_name="kling-v1-6",
    image="https://example.com/image.jpg",
    prompt="The person starts walking",
    duration="5"
)
```

### 3. Multi-Image to Video

```python
task = client.image_to_video.create(
    model_name="kling-v1-6",
    images=["img1.jpg", "img2.jpg", "img3.jpg"],
    prompt="Combine these characters in a scene",
    duration="5"
)
```

### 4. Video Extension

```python
task = client.video_extension.create(
    video_id="your-video-id",
    prompt="Continue the action"
)
```

### 5. Avatar Generation

```python
# Create audio first
tts = client.tts.create(
    text="Hello world!",
    voice_id="voice_001",
    voice_language="en"
)

# Generate avatar
task = client.avatar.create(
    image="face.jpg",
    audio_id=tts.task_result.audios[0].id
)
```

### 6. Video Effects

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

## Camera Control

```python
# Simple camera movement
task = client.text_to_video.create(
    prompt="A mountain landscape",
    camera_control={
        "type": "simple",
        "config": {
            "zoom": -5  # Zoom in (-10 to 10)
        }
    }
)

# Predefined movement
task = client.text_to_video.create(
    prompt="A cityscape",
    camera_control={"type": "forward_up"}
)
```

## Async Usage

```python
import asyncio

async def main():
    client = KlingClient(api_key="your-api-key")

    task = await client.text_to_video.create_async(
        prompt="A cat playing piano",
        duration="5"
    )

    result = await client.text_to_video.wait_for_completion_async(task.task_id)
    print(result.task_result.videos[0].url)

    await client.close_async()

asyncio.run(main())
```

## Error Handling

```python
from kling import KlingClient, KlingAPIError, KlingTimeoutError

try:
    client = KlingClient(api_key="your-api-key")
    task = client.text_to_video.create(prompt="Test")
    result = client.text_to_video.wait_for_completion(task.task_id, timeout=300)
except KlingAPIError as e:
    print(f"API Error [{e.code}]: {e.message}")
except KlingTimeoutError as e:
    print(f"Timeout: {e}")
```

## More Examples

Check out the `examples/` directory for more detailed examples:

- `examples/basic_usage.py` - Basic operations
- `examples/async_usage.py` - Async/concurrent operations
- `examples/advanced_features.py` - Camera control, lip-sync, chaining

## Environment Variables

```bash
export KLING_API_KEY="your-api-key"
```

Then in Python:

```python
import os
from kling import KlingClient

client = KlingClient(api_key=os.getenv("KLING_API_KEY"))
```

## API Endpoints by Region

```python
# Singapore (default)
client = KlingClient(
    api_key="your-key",
    base_url="https://api-singapore.klingai.com"
)

# Or use environment variable
export KLING_BASE_URL="https://api-singapore.klingai.com"
```

## Polling Configuration

```python
# Customize polling behavior
result = client.text_to_video.wait_for_completion(
    task_id=task.task_id,
    poll_interval=3.0,  # Poll every 3 seconds
    timeout=900.0       # Wait up to 15 minutes
)
```

## Context Managers

```python
# Automatic cleanup with context manager
with KlingClient(api_key="your-key") as client:
    task = client.text_to_video.create(prompt="Test")
    result = client.text_to_video.wait_for_completion(task.task_id)
# Client automatically closed

# Async context manager
async with KlingClient(api_key="your-key") as client:
    task = await client.text_to_video.create_async(prompt="Test")
    result = await client.text_to_video.wait_for_completion_async(task.task_id)
```

## Getting Help

- Check the examples in `examples/`
- Read the API documentation at the Kling AI docs
- Report issues on GitHub

Happy creating!
