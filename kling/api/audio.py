"""Audio generation APIs - Text to Audio, Video to Audio, TTS."""

from typing import List
from kling.base import BaseAPIClient
from kling.models.audio import TextToAudioRequest, VideoToAudioRequest, TTSRequest
from kling.models.common import TaskResponse, APIResponse


class TextToAudioAPI:
    """Text to audio API client."""

    def __init__(self, client: BaseAPIClient):
        self.client = client
        self.endpoint = "/v1/audio/text-to-audio"

    def create(self, **kwargs) -> TaskResponse:
        """Create a text-to-audio task."""
        request = TextToAudioRequest(**kwargs)
        data = request.model_dump(exclude_none=True)
        response = self.client.post(self.endpoint, json=data)
        api_response = APIResponse(**response)
        return api_response.data

    async def create_async(self, **kwargs) -> TaskResponse:
        request = TextToAudioRequest(**kwargs)
        data = request.model_dump(exclude_none=True)
        response = await self.client.post_async(self.endpoint, json=data)
        api_response = APIResponse(**response)
        return api_response.data

    def get(self, task_id: str) -> TaskResponse:
        endpoint = f"{self.endpoint}/{task_id}"
        response = self.client.get(endpoint)
        api_response = APIResponse(**response)
        return api_response.data

    async def get_async(self, task_id: str) -> TaskResponse:
        endpoint = f"{self.endpoint}/{task_id}"
        response = await self.client.get_async(endpoint)
        api_response = APIResponse(**response)
        return api_response.data

    def wait_for_completion(
        self, task_id: str, poll_interval: float = 5.0, timeout: float = 600.0
    ) -> TaskResponse:
        return self.client.wait_for_completion(
            task_id=task_id, get_task_func=self.get, poll_interval=poll_interval, timeout=timeout
        )

    async def wait_for_completion_async(
        self, task_id: str, poll_interval: float = 5.0, timeout: float = 600.0
    ) -> TaskResponse:
        return await self.client.wait_for_completion_async(
            task_id=task_id,
            get_task_func=self.get_async,
            poll_interval=poll_interval,
            timeout=timeout,
        )


class VideoToAudioAPI:
    """Video to audio API client."""

    def __init__(self, client: BaseAPIClient):
        self.client = client
        self.endpoint = "/v1/audio/video-to-audio"

    def create(self, **kwargs) -> TaskResponse:
        """Create a video-to-audio task."""
        request = VideoToAudioRequest(**kwargs)
        data = request.model_dump(exclude_none=True)
        response = self.client.post(self.endpoint, json=data)
        api_response = APIResponse(**response)
        return api_response.data

    async def create_async(self, **kwargs) -> TaskResponse:
        request = VideoToAudioRequest(**kwargs)
        data = request.model_dump(exclude_none=True)
        response = await self.client.post_async(self.endpoint, json=data)
        api_response = APIResponse(**response)
        return api_response.data

    def get(self, task_id: str) -> TaskResponse:
        endpoint = f"{self.endpoint}/{task_id}"
        response = self.client.get(endpoint)
        api_response = APIResponse(**response)
        return api_response.data

    async def get_async(self, task_id: str) -> TaskResponse:
        endpoint = f"{self.endpoint}/{task_id}"
        response = await self.client.get_async(endpoint)
        api_response = APIResponse(**response)
        return api_response.data

    def wait_for_completion(
        self, task_id: str, poll_interval: float = 5.0, timeout: float = 600.0
    ) -> TaskResponse:
        return self.client.wait_for_completion(
            task_id=task_id, get_task_func=self.get, poll_interval=poll_interval, timeout=timeout
        )

    async def wait_for_completion_async(
        self, task_id: str, poll_interval: float = 5.0, timeout: float = 600.0
    ) -> TaskResponse:
        return await self.client.wait_for_completion_async(
            task_id=task_id,
            get_task_func=self.get_async,
            poll_interval=poll_interval,
            timeout=timeout,
        )


class TTSAPI:
    """Text-to-speech API client."""

    def __init__(self, client: BaseAPIClient):
        self.client = client
        self.endpoint = "/v1/audio/tts"

    def create(self, **kwargs) -> TaskResponse:
        """Create a TTS task.

        Returns immediately with audio in task_result.

        Example:
            >>> result = client.tts.create(
            ...     text="Hello world",
            ...     voice_id="voice_001",
            ...     voice_language="en"
            ... )
            >>> audio_url = result.task_result.audios[0].url
        """
        request = TTSRequest(**kwargs)
        data = request.model_dump(exclude_none=True)
        response = self.client.post(self.endpoint, json=data)
        api_response = APIResponse(**response)
        return api_response.data

    async def create_async(self, **kwargs) -> TaskResponse:
        request = TTSRequest(**kwargs)
        data = request.model_dump(exclude_none=True)
        response = await self.client.post_async(self.endpoint, json=data)
        api_response = APIResponse(**response)
        return api_response.data
