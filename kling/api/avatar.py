"""Avatar API."""

from typing import List
from kling.base import BaseAPIClient
from kling.models.avatar import AvatarRequest
from kling.models.common import TaskResponse, APIResponse


class AvatarAPI:
    """Avatar API client."""

    def __init__(self, client: BaseAPIClient):
        """Initialize the avatar API."""
        self.client = client
        self.endpoint = "/v1/videos/avatar/image2video"

    def create(self, **kwargs) -> TaskResponse:
        """Create an avatar generation task.

        Args:
            **kwargs: Parameters matching AvatarRequest model

        Returns:
            Task response with task_id

        Example:
            >>> task = client.avatar.create(
            ...     image="https://example.com/face.jpg",
            ...     audio_id="audio-id-from-tts",
            ...     prompt="Speaking with emotion"
            ... )
        """
        request = AvatarRequest(**kwargs)
        data = request.model_dump(exclude_none=True)

        response = self.client.post(self.endpoint, json=data)
        api_response = APIResponse(**response)

        return api_response.data

    async def create_async(self, **kwargs) -> TaskResponse:
        """Create an avatar generation task asynchronously."""
        request = AvatarRequest(**kwargs)
        data = request.model_dump(exclude_none=True)

        response = await self.client.post_async(self.endpoint, json=data)
        api_response = APIResponse(**response)

        return api_response.data

    def get(self, task_id: str) -> TaskResponse:
        """Get task status."""
        endpoint = f"{self.endpoint}/{task_id}"
        response = self.client.get(endpoint)
        api_response = APIResponse(**response)

        return api_response.data

    async def get_async(self, task_id: str) -> TaskResponse:
        """Get task status asynchronously."""
        endpoint = f"{self.endpoint}/{task_id}"
        response = await self.client.get_async(endpoint)
        api_response = APIResponse(**response)

        return api_response.data

    def list(self, page_num: int = 1, page_size: int = 30) -> List[TaskResponse]:
        """List avatar tasks."""
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
        """List avatar tasks asynchronously."""
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
        self,
        task_id: str,
        poll_interval: float = 5.0,
        timeout: float = 600.0,
    ) -> TaskResponse:
        """Wait for task to complete."""
        return self.client.wait_for_completion(
            task_id=task_id,
            get_task_func=self.get,
            poll_interval=poll_interval,
            timeout=timeout,
        )

    async def wait_for_completion_async(
        self,
        task_id: str,
        poll_interval: float = 5.0,
        timeout: float = 600.0,
    ) -> TaskResponse:
        """Wait for task to complete asynchronously."""
        return await self.client.wait_for_completion_async(
            task_id=task_id,
            get_task_func=self.get_async,
            poll_interval=poll_interval,
            timeout=timeout,
        )
