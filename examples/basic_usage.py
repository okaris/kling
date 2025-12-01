"""Basic usage examples for Kling AI SDK."""

import os
from kling import KlingClient

# Initialize client with your access key and secret key
access_key = os.getenv("KLING_ACCESS_KEY", "ak-your-access-key")
secret_key = os.getenv("KLING_SECRET_KEY", "your-secret-key")
client = KlingClient(access_key=access_key, secret_key=secret_key)

# Example 1: Text to Video
print("=" * 50)
print("Example 1: Text to Video")
print("=" * 50)

task = client.text_to_video.create(
    model_name="kling-v2-1-master",
    prompt="A cat playing piano in a cozy living room",
    duration="5",
    mode="pro",
    aspect_ratio="16:9",
)

print(f"Task created: {task.task_id}")
print(f"Status: {task.task_status}")

# Wait for completion
print("Waiting for completion...")
result = client.text_to_video.wait_for_completion(task.task_id, poll_interval=5.0)

if result.task_status == "succeed":
    video_url = result.task_result.videos[0].url
    print(f"Video URL: {video_url}")
    print(f"Duration: {result.task_result.videos[0].duration}s")
else:
    print(f"Task failed: {result.task_status_msg}")


# Example 2: Image to Video (single image)
print("\n" + "=" * 50)
print("Example 2: Image to Video")
print("=" * 50)

task = client.image_to_video.create(
    model_name="kling-v1-6",
    image="https://example.com/image.jpg",  # Replace with your image URL
    prompt="The person starts walking forward",
    duration="5",
    mode="std",
)

print(f"Task created: {task.task_id}")


# Example 3: Multi-Image to Video
print("\n" + "=" * 50)
print("Example 3: Multi-Image to Video")
print("=" * 50)

task = client.image_to_video.create(
    model_name="kling-v1-6",
    images=[
        "https://example.com/person1.jpg",
        "https://example.com/person2.jpg",
    ],
    prompt="Two people meeting and shaking hands",
    duration="5",
)

print(f"Task created: {task.task_id}")


# Example 4: Video Extension
print("\n" + "=" * 50)
print("Example 4: Video Extension")
print("=" * 50)

# First, you need a completed video ID from a previous task
# task = client.video_extension.create(
#     video_id="your-video-id",
#     prompt="Continue the scene with more action"
# )


# Example 5: Avatar Generation
print("\n" + "=" * 50)
print("Example 5: Avatar Generation")
print("=" * 50)

# First create TTS audio
tts_result = client.tts.create(
    text="Hello! Welcome to Kling AI. I'm excited to show you what I can do.",
    voice_id="voice_001",
    voice_language="en",
    voice_speed=1.0,
)

audio_id = tts_result.task_result.audios[0].id
print(f"TTS Audio created: {audio_id}")

# Create avatar with the audio
task = client.avatar.create(
    image="https://example.com/face.jpg",
    audio_id=audio_id,
    prompt="Speaking with natural expressions",
    mode="pro",
)

print(f"Avatar task created: {task.task_id}")


# Example 6: Video Effects
print("\n" + "=" * 50)
print("Example 6: Video Effects")
print("=" * 50)

# Single-image effect
task = client.video_effects.create(
    effect_scene="pet_lion",
    input={"image": "https://example.com/cat.jpg", "duration": "5"},
)

print(f"Effect task created: {task.task_id}")

# Dual-character effect
# task = client.video_effects.create(
#     effect_scene="hug",
#     input={
#         "model_name": "kling-v1-6",
#         "mode": "std",
#         "images": [
#             "https://example.com/person1.jpg",
#             "https://example.com/person2.jpg"
#         ],
#         "duration": "5"
#     }
# )


# Example 7: Text to Audio
print("\n" + "=" * 50)
print("Example 7: Text to Audio")
print("=" * 50)

task = client.text_to_audio.create(
    prompt="Ocean waves crashing with seagulls in the background",
    duration=5.0,
)

print(f"Task created: {task.task_id}")

result = client.text_to_audio.wait_for_completion(task.task_id)
if result.task_status == "succeed":
    print(f"Audio MP3: {result.task_result.audios[0].url_mp3}")
    print(f"Audio WAV: {result.task_result.audios[0].url_wav}")


# Example 8: List tasks
print("\n" + "=" * 50)
print("Example 8: List Recent Tasks")
print("=" * 50)

tasks = client.text_to_video.list(page_num=1, page_size=5)
print(f"Found {len(tasks)} recent text-to-video tasks:")
for task in tasks:
    print(f"  - {task.task_id}: {task.task_status}")


# Clean up
client.close()
print("\n✅ Examples completed!")
