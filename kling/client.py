"""Main Kling AI Client."""

from typing import Optional
from kling.base import BaseAPIClient
from kling.api.text_to_video import TextToVideoAPI
from kling.api.image_to_video import ImageToVideoAPI
from kling.api.video_extension import VideoExtensionAPI
from kling.api.avatar import AvatarAPI
from kling.api.lip_sync import LipSyncAPI
from kling.api.video_effects import VideoEffectsAPI
from kling.api.audio import TextToAudioAPI, VideoToAudioAPI, TTSAPI


class KlingClient:
    """Main Kling AI client.

    Provides access to all Kling AI APIs through a unified interface.

    Example:
        >>> client = KlingClient(
        ...     access_key="ak-your-access-key",
        ...     secret_key="your-secret-key"
        ... )
        >>>
        >>> # Generate video from text
        >>> task = client.text_to_video.create(
        ...     model_name="kling-v2-1-master",
        ...     prompt="A beautiful sunset",
        ...     duration="5"
        ... )
        >>> result = client.text_to_video.wait_for_completion(task.task_id)
        >>> print(result.task_result.videos[0].url)
        >>>
        >>> # Generate video from image
        >>> task = client.image_to_video.create(
        ...     image="https://example.com/image.jpg",
        ...     prompt="The person starts walking"
        ... )
        >>>
        >>> # Multi-image to video
        >>> task = client.image_to_video.create(
        ...     images=["img1.jpg", "img2.jpg"],
        ...     prompt="Two people meeting"
        ... )
        >>>
        >>> # Create avatar
        >>> task = client.avatar.create(
        ...     image="face.jpg",
        ...     audio_id="audio-id"
        ... )
        >>>
        >>> # Apply video effect
        >>> task = client.video_effects.create(
        ...     effect_scene="pet_lion",
        ...     input={"image": "cat.jpg", "duration": "5"}
        ... )
    """

    def __init__(
        self,
        access_key: str,
        secret_key: str,
        base_url: str = "https://api-singapore.klingai.com",
        timeout: float = 30.0,
        max_retries: int = 3,
    ):
        """Initialize the Kling AI client.

        Args:
            access_key: Your Kling AI Access Key (ak-xxx)
            secret_key: Your Kling AI Secret Key
            base_url: Base URL for the API (default: Singapore endpoint)
            timeout: Request timeout in seconds (default: 30)
            max_retries: Maximum retry attempts (default: 3)
        """
        self._base_client = BaseAPIClient(
            access_key=access_key,
            secret_key=secret_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
        )

        # Initialize all API endpoints
        self.text_to_video = TextToVideoAPI(self._base_client)
        self.image_to_video = ImageToVideoAPI(self._base_client)
        self.video_extension = VideoExtensionAPI(self._base_client)
        self.avatar = AvatarAPI(self._base_client)
        self.lip_sync = LipSyncAPI(self._base_client)
        self.video_effects = VideoEffectsAPI(self._base_client)
        self.text_to_audio = TextToAudioAPI(self._base_client)
        self.video_to_audio = VideoToAudioAPI(self._base_client)
        self.tts = TTSAPI(self._base_client)

    def close(self):
        """Close HTTP clients."""
        self._base_client.close()

    async def close_async(self):
        """Close async HTTP client."""
        await self._base_client.close_async()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close_async()
