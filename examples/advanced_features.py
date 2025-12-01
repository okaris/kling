"""Advanced features: camera control, motion brush, lip-sync."""

import os
from kling import KlingClient

api_key = os.getenv("KLING_API_KEY", "your-api-key-here")
client = KlingClient(api_key=api_key)


# Example 1: Camera Control
print("=" * 50)
print("Example 1: Camera Control")
print("=" * 50)

# Simple camera movement (zoom in)
task = client.text_to_video.create(
    model_name="kling-v2-1-master",
    prompt="A mountain landscape",
    duration="5",
    camera_control={
        "type": "simple",
        "config": {
            "horizontal": 0,
            "vertical": 0,
            "pan": 0,
            "tilt": 0,
            "roll": 0,
            "zoom": -5,  # Zoom in
        },
    },
)

print(f"Task with camera zoom: {task.task_id}")

# Predefined camera movement
task = client.text_to_video.create(
    model_name="kling-v2-1-master",
    prompt="A cityscape",
    duration="5",
    camera_control={"type": "forward_up"},  # Zoom in and pan up
)

print(f"Task with forward_up camera: {task.task_id}")


# Example 2: Image to Video with Motion Brush (Dynamic Masks)
print("\n" + "=" * 50)
print("Example 2: Motion Brush (Dynamic Masks)")
print("=" * 50)

task = client.image_to_video.create(
    model_name="kling-v1",
    image="https://example.com/scene.jpg",
    prompt="The object moves along the path",
    duration="5",
    mode="std",
    dynamic_masks=[
        {
            "mask": "https://example.com/mask.png",  # Mask showing what to move
            "trajectories": [
                {"x": 100, "y": 200},  # Start position
                {"x": 300, "y": 200},  # End position
            ],
        }
    ],
)

print(f"Task with motion brush: {task.task_id}")


# Example 3: Static Mask
print("\n" + "=" * 50)
print("Example 3: Static Mask")
print("=" * 50)

task = client.image_to_video.create(
    model_name="kling-v1",
    image="https://example.com/image.jpg",
    prompt="Everything except the masked area moves",
    duration="5",
    static_mask="https://example.com/static_mask.png",  # Area that stays still
)

print(f"Task with static mask: {task.task_id}")


# Example 4: End Frame Control (Image to Image)
print("\n" + "=" * 50)
print("Example 4: End Frame Control")
print("=" * 50)

task = client.image_to_video.create(
    model_name="kling-v1",
    image="https://example.com/start_frame.jpg",
    image_tail="https://example.com/end_frame.jpg",
    prompt="Smooth transition between frames",
    duration="5",
)

print(f"Task with end frame: {task.task_id}")


# Example 5: Advanced Lip Sync
print("\n" + "=" * 50)
print("Example 5: Advanced Lip Sync")
print("=" * 50)

# Step 1: Identify faces in the video
faces = client.lip_sync.identify_faces(video_id="your-video-id")

print(f"Session ID: {faces.session_id}")
print(f"Found {len(faces.face_data)} faces:")
for face in faces.face_data:
    print(f"  - Face ID: {face.face_id}")
    print(f"    Time range: {face.start_time}ms - {face.end_time}ms")
    print(f"    Preview: {face.face_image}")

# Step 2: Create TTS audio
tts_result = client.tts.create(
    text="Hello, this is a lip-sync test!",
    voice_id="voice_001",
    voice_language="en",
)

audio_id = tts_result.task_result.audios[0].id
audio_duration_ms = int(float(tts_result.task_result.audios[0].duration) * 1000)

# Step 3: Apply lip-sync to the first face
task = client.lip_sync.create(
    session_id=faces.session_id,
    face_choose=[
        {
            "face_id": faces.face_data[0].face_id,
            "audio_id": audio_id,
            "sound_start_time": 0,  # Start from beginning of audio
            "sound_end_time": audio_duration_ms,  # Use full audio
            "sound_insert_time": faces.face_data[0].start_time,  # Insert at face start
            "sound_volume": 1.5,  # Boost audio volume
            "original_audio_volume": 0.3,  # Reduce original audio
        }
    ],
)

print(f"Lip-sync task created: {task.task_id}")


# Example 6: Video to Audio with ASMR Mode
print("\n" + "=" * 50)
print("Example 6: Video to Audio with ASMR")
print("=" * 50)

task = client.video_to_audio.create(
    video_id="your-video-id",
    sound_effect_prompt="Detailed ambient sounds and footsteps",
    bgm_prompt="Calm, soothing background music",
    asmr_mode=True,  # Enhanced detail for immersive audio
)

print(f"Video to audio task: {task.task_id}")

result = client.video_to_audio.wait_for_completion(task.task_id)
if result.task_status == "succeed":
    print(f"Video with audio: {result.task_result.videos[0].url}")
    print(f"Audio only (MP3): {result.task_result.audios[0].url_mp3}")


# Example 7: Chaining Operations
print("\n" + "=" * 50)
print("Example 7: Chaining Operations")
print("=" * 50)

# Create initial video
task1 = client.text_to_video.create(
    model_name="kling-v2-1-master",
    prompt="A person walking in a park",
    duration="5",
)

result1 = client.text_to_video.wait_for_completion(task1.task_id)
video_id = result1.task_result.videos[0].id

# Extend it
task2 = client.video_extension.create(
    video_id=video_id, prompt="The person continues walking and sits on a bench"
)

result2 = client.video_extension.wait_for_completion(task2.task_id)
extended_video_id = result2.task_result.videos[0].id

# Add audio
task3 = client.video_to_audio.create(
    video_id=extended_video_id,
    sound_effect_prompt="Birds chirping, footsteps on grass",
    bgm_prompt="Peaceful ambient music",
)

result3 = client.video_to_audio.wait_for_completion(task3.task_id)
final_video_url = result3.task_result.videos[0].url

print(f"Final video with extended duration and audio: {final_video_url}")


client.close()
print("\n✅ Advanced examples completed!")
