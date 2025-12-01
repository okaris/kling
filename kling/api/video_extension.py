"""Video Extension API."""

from typing import List
from kling.base import BaseAPIClient
from kling.models.video import VideoExtensionRequest
from kling.models.common import TaskResponse, APIResponse


class VideoExtensionAPI:
    """Video extension API client."""

    def __init__(self, client: BaseAPIClient):
        """Initialize the video extension API.

        Args:
            client: Base API client instance
        """
        self.client = client
        self.endpoint = "/v1/videos/video-extend"

    def create(self, **kwargs) -> TaskResponse:
        """Create a video extension task.

        Extends an existing video by 4-5 seconds. Can be used multiple times
        but total duration cannot exceed 3 minutes.

        Args:
            **kwargs: Parameters matching VideoExtensionRequest model

        Returns:
            Task response with task_id

        Example:
            >>> task = client.video_extension.create(
            ...     video_id="existing-video-id",
            ...     prompt="Continue the scene"
            ... )
        """
        request = VideoExtensionRequest(**kwargs)
        data = request.model_dump(exclude_none=True)

        response = self.client.post(self.endpoint, json=data)
        api_response = APIResponse(**response)

        return api_response.data

    async def create_async(self, **kwargs) -> TaskResponse:
        """Create a video extension task asynchronously."""
        request = VideoExtensionRequest(**kwargs)
        data = request.model_dump(exclude_none=True)

        response = await self.client.post_async(self.endpoint, json=data)
        api_response = APIResponse(**response)

        return api_response.data

    def get(self, task_id: str) -> TaskResponse:
        """Get task status.

        Args:
            task_id: Task ID

        Returns:
            Task response with current status
        """
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
        """List video extension tasks.

        Args:
            page_num: Page number (1-1000)
            page_size: Items per page (1-500)

        Returns:
            List of task responses
        """
        params = {"pageNum": page_num, "pageSize": page_size}
        response = self.client.get(self.endpoint, params=params)

        code = response.get("code", 0)
        message = response.get("message", "")
        request_id = response.get("request_id", "")

        if code != 0:
            from kling.exceptions import KlingAPIError

            raise KlingAPIError(message=message, code=code, request_id=request_id)

        data = response.get("data", [])
        return [TaskResponse(**item) for item in data]

    async def list_async(self, page_num: int = 1, page_size: int = 30) -> List[TaskResponse]:
        """List video extension tasks asynchronously."""
        params = {"pageNum": page_num, "pageSize": page_size}
        response = await self.client.get_async(self.endpoint, params=params)

        code = response.get("code", 0)
        message = response.get("message", "")
        request_id = response.get("request_id", "")

        if code != 0:
            from kling.exceptions import KlingAPIError

            raise KlingAPIError(message=message, code=code, request_id=request_id)

        data = response.get("data", [])
        return [TaskResponse(**item) for item in data]

    def wait_for_completion(
        self,
        task_id: str,
        poll_interval: float = 5.0,
        timeout: float = 600.0,
    ) -> TaskResponse:
        """Wait for task to complete.

        Args:
            task_id: Task ID to wait for
            poll_interval: Seconds between polls (default: 5)
            timeout: Maximum wait time in seconds (default: 600)

        Returns:
            Completed task response
        """
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
