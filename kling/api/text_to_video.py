"""Text to Video API."""

from typing import Optional, List
from kling.base import BaseAPIClient
from kling.models.video import TextToVideoRequest
from kling.models.common import TaskResponse, APIResponse


class TextToVideoAPI:
    """Text to video API client."""

    def __init__(self, client: BaseAPIClient):
        """Initialize the text to video API.

        Args:
            client: Base API client instance
        """
        self.client = client
        self.endpoint = "/v1/videos/text2video"

    def create(self, **kwargs) -> TaskResponse:
        """Create a text-to-video task.

        Args:
            **kwargs: Parameters matching TextToVideoRequest model

        Returns:
            Task response with task_id

        Example:
            >>> task = client.text_to_video.create(
            ...     model_name="kling-v2-1-master",
            ...     prompt="A cat playing piano",
            ...     duration="5",
            ...     mode="pro"
            ... )
            >>> print(task.task_id)
        """
        # Validate and serialize request
        request = TextToVideoRequest(**kwargs)
        data = request.model_dump(exclude_none=True)

        # Make API call
        response = self.client.post(self.endpoint, json=data)
        api_response = APIResponse(**response)

        return api_response.data

    async def create_async(self, **kwargs) -> TaskResponse:
        """Create a text-to-video task asynchronously.

        Args:
            **kwargs: Parameters matching TextToVideoRequest model

        Returns:
            Task response with task_id
        """
        request = TextToVideoRequest(**kwargs)
        data = request.model_dump(exclude_none=True)

        response = await self.client.post_async(self.endpoint, json=data)
        api_response = APIResponse(**response)

        return api_response.data

    def get(self, task_id: str) -> TaskResponse:
        """Get task status by task_id.

        Args:
            task_id: Task ID or external_task_id

        Returns:
            Task response with current status

        Example:
            >>> task = client.text_to_video.get("task-id-123")
            >>> print(task.task_status)
        """
        endpoint = f"{self.endpoint}/{task_id}"
        response = self.client.get(endpoint)
        api_response = APIResponse(**response)

        return api_response.data

    async def get_async(self, task_id: str) -> TaskResponse:
        """Get task status asynchronously.

        Args:
            task_id: Task ID or external_task_id

        Returns:
            Task response with current status
        """
        endpoint = f"{self.endpoint}/{task_id}"
        response = await self.client.get_async(endpoint)
        api_response = APIResponse(**response)

        return api_response.data

    def list(self, page_num: int = 1, page_size: int = 30) -> List[TaskResponse]:
        """List text-to-video tasks.

        Args:
            page_num: Page number (1-1000)
            page_size: Items per page (1-500)

        Returns:
            List of task responses

        Example:
            >>> tasks = client.text_to_video.list(page_num=1, page_size=10)
            >>> for task in tasks:
            ...     print(task.task_id, task.task_status)
        """
        params = {"pageNum": page_num, "pageSize": page_size}
        response = self.client.get(self.endpoint, params=params)

        # Parse response - data is a list for list endpoints
        code = response.get("code", 0)
        message = response.get("message", "")
        request_id = response.get("request_id", "")

        if code != 0:
            from kling.exceptions import KlingAPIError

            raise KlingAPIError(message=message, code=code, request_id=request_id)

        data = response.get("data", [])
        return [TaskResponse(**item) for item in data]

    async def list_async(self, page_num: int = 1, page_size: int = 30) -> List[TaskResponse]:
        """List text-to-video tasks asynchronously.

        Args:
            page_num: Page number (1-1000)
            page_size: Items per page (1-500)

        Returns:
            List of task responses
        """
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

        Example:
            >>> task = client.text_to_video.create(prompt="...")
            >>> result = client.text_to_video.wait_for_completion(task.task_id)
            >>> video_url = result.task_result.videos[0].url
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
        """Wait for task to complete asynchronously.

        Args:
            task_id: Task ID to wait for
            poll_interval: Seconds between polls (default: 5)
            timeout: Maximum wait time in seconds (default: 600)

        Returns:
            Completed task response
        """
        return await self.client.wait_for_completion_async(
            task_id=task_id,
            get_task_func=self.get_async,
            poll_interval=poll_interval,
            timeout=timeout,
        )
