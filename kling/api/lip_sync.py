"""Lip Sync API."""

from typing import List
from kling.base import BaseAPIClient
from kling.models.avatar import (
    IdentifyFaceRequest,
    IdentifyFaceResponse,
    LipSyncRequest,
)
from kling.models.common import TaskResponse, APIResponse


class LipSyncAPI:
    """Lip-sync API client."""

    def __init__(self, client: BaseAPIClient):
        """Initialize the lip-sync API."""
        self.client = client
        self.identify_endpoint = "/v1/videos/Identify-face"
        self.lipsync_endpoint = "/v1/videos/advanced-lip-sync"

    def identify_faces(self, **kwargs) -> IdentifyFaceResponse:
        """Identify faces in a video.

        Args:
            **kwargs: video_id or video_url

        Returns:
            IdentifyFaceResponse with session_id and face_data

        Example:
            >>> faces = client.lip_sync.identify_faces(video_id="video-id")
            >>> print(faces.session_id)
            >>> for face in faces.face_data:
            ...     print(face.face_id, face.start_time, face.end_time)
        """
        request = IdentifyFaceRequest(**kwargs)
        data = request.model_dump(exclude_none=True)

        response = self.client.post(self.identify_endpoint, json=data)

        code = response.get("code", 0)
        if code != 0:
            from kling.exceptions import KlingAPIError

            raise KlingAPIError(
                message=response.get("message", ""),
                code=code,
                request_id=response.get("request_id", ""),
            )

        return IdentifyFaceResponse(**response.get("data", {}))

    async def identify_faces_async(self, **kwargs) -> IdentifyFaceResponse:
        """Identify faces in a video asynchronously."""
        request = IdentifyFaceRequest(**kwargs)
        data = request.model_dump(exclude_none=True)

        response = await self.client.post_async(self.identify_endpoint, json=data)

        code = response.get("code", 0)
        if code != 0:
            from kling.exceptions import KlingAPIError

            raise KlingAPIError(
                message=response.get("message", ""),
                code=code,
                request_id=response.get("request_id", ""),
            )

        return IdentifyFaceResponse(**response.get("data", {}))

    def create(self, **kwargs) -> TaskResponse:
        """Create a lip-sync task.

        Args:
            **kwargs: Parameters matching LipSyncRequest model

        Returns:
            Task response with task_id

        Example:
            >>> faces = client.lip_sync.identify_faces(video_id="video-id")
            >>> task = client.lip_sync.create(
            ...     session_id=faces.session_id,
            ...     face_choose=[{
            ...         "face_id": faces.face_data[0].face_id,
            ...         "audio_id": "audio-id",
            ...         "sound_start_time": 0,
            ...         "sound_end_time": 5000,
            ...         "sound_insert_time": 0
            ...     }]
            ... )
        """
        request = LipSyncRequest(**kwargs)
        data = request.model_dump(exclude_none=True)

        response = self.client.post(self.lipsync_endpoint, json=data)
        api_response = APIResponse(**response)

        return api_response.data

    async def create_async(self, **kwargs) -> TaskResponse:
        """Create a lip-sync task asynchronously."""
        request = LipSyncRequest(**kwargs)
        data = request.model_dump(exclude_none=True)

        response = await self.client.post_async(self.lipsync_endpoint, json=data)
        api_response = APIResponse(**response)

        return api_response.data

    def get(self, task_id: str) -> TaskResponse:
        """Get task status."""
        endpoint = f"{self.lipsync_endpoint}/{task_id}"
        response = self.client.get(endpoint)
        api_response = APIResponse(**response)

        return api_response.data

    async def get_async(self, task_id: str) -> TaskResponse:
        """Get task status asynchronously."""
        endpoint = f"{self.lipsync_endpoint}/{task_id}"
        response = await self.client.get_async(endpoint)
        api_response = APIResponse(**response)

        return api_response.data

    def list(self, page_num: int = 1, page_size: int = 30) -> List[TaskResponse]:
        """List lip-sync tasks."""
        params = {"pageNum": page_num, "pageSize": page_size}
        response = self.client.get(self.lipsync_endpoint, params=params)

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
        """List lip-sync tasks asynchronously."""
        params = {"pageNum": page_num, "pageSize": page_size}
        response = await self.client.get_async(self.lipsync_endpoint, params=params)

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
