"""Image to Video API - Handles single and multi-image to video."""

from typing import Optional, List, Union
from kling.base import BaseAPIClient
from kling.models.video import (
    ImageToVideoRequest,
    MultiImageToVideoRequest,
    ImageInput,
)
from kling.models.common import TaskResponse, APIResponse


class ImageToVideoAPI:
    """Image to video API client.

    Supports both single image-to-video and multi-image-to-video (Elements).
    Automatically routes to the correct endpoint based on input.
    """

    def __init__(self, client: BaseAPIClient):
        """Initialize the image to video API.

        Args:
            client: Base API client instance
        """
        self.client = client
        self.single_endpoint = "/v1/videos/image2video"
        self.multi_endpoint = "/v1/videos/multi-image2video"

    def create(
        self,
        image: Optional[str] = None,
        images: Optional[List[Union[str, dict, ImageInput]]] = None,
        image_list: Optional[List[Union[str, dict, ImageInput]]] = None,
        **kwargs,
    ) -> TaskResponse:
        """Create an image-to-video task.

        Automatically detects single vs multi-image based on parameters.

        Args:
            image: Single image URL or Base64 (for single image mode)
            images: Multiple images (for multi-image mode)
            image_list: Multiple images (alternative parameter name)
            **kwargs: Additional parameters

        Returns:
            Task response with task_id

        Example (single image):
            >>> task = client.image_to_video.create(
            ...     model_name="kling-v1-6",
            ...     image="https://example.com/image.jpg",
            ...     prompt="The person starts walking"
            ... )

        Example (multi-image):
            >>> task = client.image_to_video.create(
            ...     model_name="kling-v1-6",
            ...     images=["https://example.com/img1.jpg", "https://example.com/img2.jpg"],
            ...     prompt="Two people meeting"
            ... )
        """
        # Determine if this is single or multi-image
        multi_images = images or image_list

        if multi_images:
            # Multi-image mode
            return self._create_multi_image(images=multi_images, **kwargs)
        else:
            # Single image mode
            return self._create_single_image(image=image, **kwargs)

    async def create_async(
        self,
        image: Optional[str] = None,
        images: Optional[List[Union[str, dict, ImageInput]]] = None,
        image_list: Optional[List[Union[str, dict, ImageInput]]] = None,
        **kwargs,
    ) -> TaskResponse:
        """Create an image-to-video task asynchronously."""
        multi_images = images or image_list

        if multi_images:
            return await self._create_multi_image_async(images=multi_images, **kwargs)
        else:
            return await self._create_single_image_async(image=image, **kwargs)

    def _create_single_image(self, **kwargs) -> TaskResponse:
        """Create single image-to-video task."""
        request = ImageToVideoRequest(**kwargs)
        data = request.model_dump(exclude_none=True)

        response = self.client.post(self.single_endpoint, json=data)
        api_response = APIResponse(**response)

        return api_response.data

    async def _create_single_image_async(self, **kwargs) -> TaskResponse:
        """Create single image-to-video task asynchronously."""
        request = ImageToVideoRequest(**kwargs)
        data = request.model_dump(exclude_none=True)

        response = await self.client.post_async(self.single_endpoint, json=data)
        api_response = APIResponse(**response)

        return api_response.data

    def _create_multi_image(self, images: List[Union[str, dict, ImageInput]], **kwargs) -> TaskResponse:
        """Create multi-image-to-video task."""
        # Normalize images to ImageInput format
        normalized_images = []
        for img in images:
            if isinstance(img, str):
                normalized_images.append(ImageInput(image=img))
            elif isinstance(img, dict):
                normalized_images.append(ImageInput(**img))
            else:
                normalized_images.append(img)

        request = MultiImageToVideoRequest(image_list=normalized_images, **kwargs)
        data = request.model_dump(exclude_none=True)

        response = self.client.post(self.multi_endpoint, json=data)
        api_response = APIResponse(**response)

        return api_response.data

    async def _create_multi_image_async(
        self, images: List[Union[str, dict, ImageInput]], **kwargs
    ) -> TaskResponse:
        """Create multi-image-to-video task asynchronously."""
        normalized_images = []
        for img in images:
            if isinstance(img, str):
                normalized_images.append(ImageInput(image=img))
            elif isinstance(img, dict):
                normalized_images.append(ImageInput(**img))
            else:
                normalized_images.append(img)

        request = MultiImageToVideoRequest(image_list=normalized_images, **kwargs)
        data = request.model_dump(exclude_none=True)

        response = await self.client.post_async(self.multi_endpoint, json=data)
        api_response = APIResponse(**response)

        return api_response.data

    def get(self, task_id: str, multi_image: bool = False) -> TaskResponse:
        """Get task status.

        Args:
            task_id: Task ID or external_task_id
            multi_image: Whether this is a multi-image task

        Returns:
            Task response with current status
        """
        endpoint = self.multi_endpoint if multi_image else self.single_endpoint
        endpoint = f"{endpoint}/{task_id}"

        response = self.client.get(endpoint)
        api_response = APIResponse(**response)

        return api_response.data

    async def get_async(self, task_id: str, multi_image: bool = False) -> TaskResponse:
        """Get task status asynchronously."""
        endpoint = self.multi_endpoint if multi_image else self.single_endpoint
        endpoint = f"{endpoint}/{task_id}"

        response = await self.client.get_async(endpoint)
        api_response = APIResponse(**response)

        return api_response.data

    def list(
        self, page_num: int = 1, page_size: int = 30, multi_image: bool = False
    ) -> List[TaskResponse]:
        """List image-to-video tasks.

        Args:
            page_num: Page number (1-1000)
            page_size: Items per page (1-500)
            multi_image: Whether to list multi-image tasks

        Returns:
            List of task responses
        """
        endpoint = self.multi_endpoint if multi_image else self.single_endpoint
        params = {"pageNum": page_num, "pageSize": page_size}
        response = self.client.get(endpoint, params=params)

        code = response.get("code", 0)
        message = response.get("message", "")
        request_id = response.get("request_id", "")

        if code != 0:
            from kling.exceptions import KlingAPIError

            raise KlingAPIError(message=message, code=code, request_id=request_id)

        data = response.get("data", [])
        return [TaskResponse(**item) for item in data]

    async def list_async(
        self, page_num: int = 1, page_size: int = 30, multi_image: bool = False
    ) -> List[TaskResponse]:
        """List image-to-video tasks asynchronously."""
        endpoint = self.multi_endpoint if multi_image else self.single_endpoint
        params = {"pageNum": page_num, "pageSize": page_size}
        response = await self.client.get_async(endpoint, params=params)

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
        multi_image: bool = False,
        poll_interval: float = 5.0,
        timeout: float = 600.0,
    ) -> TaskResponse:
        """Wait for task to complete.

        Args:
            task_id: Task ID to wait for
            multi_image: Whether this is a multi-image task
            poll_interval: Seconds between polls (default: 5)
            timeout: Maximum wait time in seconds (default: 600)

        Returns:
            Completed task response
        """

        def get_task(tid: str) -> TaskResponse:
            return self.get(tid, multi_image=multi_image)

        return self.client.wait_for_completion(
            task_id=task_id,
            get_task_func=get_task,
            poll_interval=poll_interval,
            timeout=timeout,
        )

    async def wait_for_completion_async(
        self,
        task_id: str,
        multi_image: bool = False,
        poll_interval: float = 5.0,
        timeout: float = 600.0,
    ) -> TaskResponse:
        """Wait for task to complete asynchronously."""

        async def get_task(tid: str) -> TaskResponse:
            return await self.get_async(tid, multi_image=multi_image)

        return await self.client.wait_for_completion_async(
            task_id=task_id,
            get_task_func=get_task,
            poll_interval=poll_interval,
            timeout=timeout,
        )
