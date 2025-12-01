"""Video Effects API."""

from typing import List
from kling.base import BaseAPIClient
from kling.models.effects import VideoEffectsRequest
from kling.models.common import TaskResponse, APIResponse


class VideoEffectsAPI:
    """Video effects API client."""

    def __init__(self, client: BaseAPIClient):
        self.client = client
        self.endpoint = "/v1/videos/effects"

    def create(self, effect_scene: str, input: dict, **kwargs) -> TaskResponse:
        """Create a video effects task.

        Args:
            effect_scene: Effect scene name (e.g., "pet_lion", "hug", "kiss")
            input: Effect input parameters (varies by effect type)
            **kwargs: Additional parameters (callback_url, external_task_id)

        Returns:
            Task response with task_id

        Example (single image effect):
            >>> task = client.video_effects.create(
            ...     effect_scene="pet_lion",
            ...     input={"image": "https://example.com/img.jpg", "duration": "5"}
            ... )

        Example (dual character effect):
            >>> task = client.video_effects.create(
            ...     effect_scene="hug",
            ...     input={
            ...         "model_name": "kling-v1-6",
            ...         "mode": "std",
            ...         "images": ["img1.jpg", "img2.jpg"],
            ...         "duration": "5"
            ...     }
            ... )
        """
        request = VideoEffectsRequest(effect_scene=effect_scene, input=input, **kwargs)
        data = request.model_dump(exclude_none=True)
        response = self.client.post(self.endpoint, json=data)
        api_response = APIResponse(**response)
        return api_response.data

    async def create_async(self, effect_scene: str, input: dict, **kwargs) -> TaskResponse:
        request = VideoEffectsRequest(effect_scene=effect_scene, input=input, **kwargs)
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

    def list(self, page_num: int = 1, page_size: int = 30) -> List[TaskResponse]:
        params = {"pageNum": page_num, "pageSize": page_size}
        response = self.client.get(self.endpoint, params=params)

        code = response.get("code", 0)
        if code != 0:
            from kling.exceptions import KlingAPIError

            raise KlingAPIError(
                message=response.get("message", ""),
                code=code,
                request_id=response.get("request_id", ""),
            )

        data = response.get("data", [])
        return [TaskResponse(**item) for item in data]

    async def list_async(self, page_num: int = 1, page_size: int = 30) -> List[TaskResponse]:
        params = {"pageNum": page_num, "pageSize": page_size}
        response = await self.client.get_async(self.endpoint, params=params)

        code = response.get("code", 0)
        if code != 0:
            from kling.exceptions import KlingAPIError

            raise KlingAPIError(
                message=response.get("message", ""),
                code=code,
                request_id=response.get("request_id", ""),
            )

        data = response.get("data", [])
        return [TaskResponse(**item) for item in data]

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
