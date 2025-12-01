"""Async usage examples for Kling AI SDK."""

import asyncio
import os
from kling import KlingClient


async def main():
    # Initialize client
    access_key = os.getenv("KLING_ACCESS_KEY", "ak-your-access-key")
    secret_key = os.getenv("KLING_SECRET_KEY", "your-secret-key")
    client = KlingClient(access_key=access_key, secret_key=secret_key)

    # Example 1: Create multiple videos concurrently
    print("=" * 50)
    print("Creating 3 videos concurrently")
    print("=" * 50)

    prompts = [
        "A cat playing piano",
        "A sunset over mountains",
        "Waves crashing on a beach",
    ]

    # Create all tasks concurrently
    tasks = await asyncio.gather(
        *[
            client.text_to_video.create_async(
                model_name="kling-v2-1-master",
                prompt=prompt,
                duration="5",
                mode="std",
            )
            for prompt in prompts
        ]
    )

    print(f"Created {len(tasks)} tasks:")
    for i, task in enumerate(tasks):
        print(f"  {i+1}. {task.task_id} - {prompts[i]}")

    # Wait for all to complete
    print("\nWaiting for all tasks to complete...")
    results = await asyncio.gather(
        *[
            client.text_to_video.wait_for_completion_async(task.task_id, poll_interval=5.0)
            for task in tasks
        ]
    )

    print("\n✅ All tasks completed!")
    for i, result in enumerate(results):
        if result.task_status == "succeed":
            video_url = result.task_result.videos[0].url
            print(f"  {i+1}. {prompts[i]}")
            print(f"     URL: {video_url}")
        else:
            print(f"  {i+1}. Failed: {result.task_status_msg}")

    # Example 2: Image to Video with async
    print("\n" + "=" * 50)
    print("Async Image to Video")
    print("=" * 50)

    task = await client.image_to_video.create_async(
        model_name="kling-v1-6",
        image="https://example.com/image.jpg",
        prompt="The scene comes to life",
        duration="5",
    )

    print(f"Task created: {task.task_id}")

    result = await client.image_to_video.wait_for_completion_async(task.task_id)
    if result.task_status == "succeed":
        print(f"Video URL: {result.task_result.videos[0].url}")

    # Example 3: Avatar with async
    print("\n" + "=" * 50)
    print("Async Avatar Generation")
    print("=" * 50)

    # Create TTS audio
    tts_result = await client.tts.create_async(
        text="Hello from the async world!",
        voice_id="voice_001",
        voice_language="en",
    )

    audio_id = tts_result.task_result.audios[0].id

    # Create avatar
    task = await client.avatar.create_async(
        image="https://example.com/face.jpg",
        audio_id=audio_id,
        prompt="Speaking cheerfully",
    )

    print(f"Avatar task created: {task.task_id}")

    # Clean up
    await client.close_async()
    print("\n✅ Async examples completed!")


if __name__ == "__main__":
    asyncio.run(main())
