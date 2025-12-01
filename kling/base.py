"""Base API client with authentication and polling logic."""

import time
import jwt
from typing import Optional, Dict, Any, Callable
import httpx
from kling.exceptions import KlingAPIError, KlingTimeoutError
from kling.models.common import APIResponse, TaskResponse, TaskStatus


class BaseAPIClient:
    """Base API client with common functionality."""

    def __init__(
        self,
        access_key: str,
        secret_key: str,
        base_url: str = "https://api-singapore.klingai.com",
        timeout: float = 30.0,
        max_retries: int = 3,
    ):
        """Initialize the base API client.

        Args:
            access_key: Kling AI Access Key (ak-xxx)
            secret_key: Kling AI Secret Key
            base_url: Base URL for the API
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
        """
        self.access_key = access_key
        self.secret_key = secret_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries

        # Create HTTP clients
        self._client = httpx.Client(timeout=timeout)
        self._async_client = httpx.AsyncClient(timeout=timeout)

    def _generate_jwt_token(self) -> str:
        """Generate JWT token for API authentication."""
        now = int(time.time())
        payload = {
            "iss": self.access_key,
            "exp": now + 1800,  # Token expires in 30 minutes
            "nbf": now - 5,  # Token valid from 5 seconds ago
        }
        return jwt.encode(payload, self.secret_key, algorithm="HS256")

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with authentication."""
        token = self._generate_jwt_token()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        """Handle API response and raise errors if needed."""
        try:
            data = response.json()
        except Exception:
            raise KlingAPIError(
                message="Invalid JSON response from API",
                code=-1,
                request_id="",
            )

        # Check for API errors
        if data.get("code", 0) != 0:
            raise KlingAPIError(
                message=data.get("message", "Unknown error"),
                code=data.get("code", -1),
                request_id=data.get("request_id", ""),
            )

        return data

    def post(self, endpoint: str, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a POST request.

        Args:
            endpoint: API endpoint (e.g., "/v1/videos/text2video")
            json: Request body as dictionary

        Returns:
            Response data as dictionary
        """
        url = f"{self.base_url}{endpoint}"
        response = self._client.post(url, headers=self._get_headers(), json=json)
        return self._handle_response(response)

    async def post_async(
        self, endpoint: str, json: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make an async POST request.

        Args:
            endpoint: API endpoint
            json: Request body as dictionary

        Returns:
            Response data as dictionary
        """
        url = f"{self.base_url}{endpoint}"
        response = await self._async_client.post(url, headers=self._get_headers(), json=json)
        return self._handle_response(response)

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a GET request.

        Args:
            endpoint: API endpoint
            params: Query parameters

        Returns:
            Response data as dictionary
        """
        url = f"{self.base_url}{endpoint}"
        response = self._client.get(url, headers=self._get_headers(), params=params)
        return self._handle_response(response)

    async def get_async(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make an async GET request.

        Args:
            endpoint: API endpoint
            params: Query parameters

        Returns:
            Response data as dictionary
        """
        url = f"{self.base_url}{endpoint}"
        response = await self._async_client.get(url, headers=self._get_headers(), params=params)
        return self._handle_response(response)

    def wait_for_completion(
        self,
        task_id: str,
        get_task_func: Callable[[str], TaskResponse],
        poll_interval: float = 5.0,
        timeout: float = 600.0,
    ) -> TaskResponse:
        """Poll a task until it completes.

        Args:
            task_id: Task ID to poll
            get_task_func: Function to get task status
            poll_interval: Seconds between poll attempts
            timeout: Maximum seconds to wait

        Returns:
            Completed task response

        Raises:
            KlingTimeoutError: If task doesn't complete within timeout
            KlingAPIError: If task fails
        """
        start_time = time.time()

        while True:
            task = get_task_func(task_id)

            if task.task_status == "succeed":
                return task
            elif task.task_status == "failed":
                raise KlingAPIError(
                    message=task.task_status_msg or "Task failed",
                    code=-1,
                    request_id="",
                )

            # Check timeout
            elapsed = time.time() - start_time
            if elapsed >= timeout:
                raise KlingTimeoutError(
                    f"Task {task_id} did not complete within {timeout} seconds"
                )

            # Wait before next poll
            time.sleep(poll_interval)

    async def wait_for_completion_async(
        self,
        task_id: str,
        get_task_func: Callable[[str], Any],
        poll_interval: float = 5.0,
        timeout: float = 600.0,
    ) -> TaskResponse:
        """Async poll a task until it completes.

        Args:
            task_id: Task ID to poll
            get_task_func: Async function to get task status
            poll_interval: Seconds between poll attempts
            timeout: Maximum seconds to wait

        Returns:
            Completed task response

        Raises:
            KlingTimeoutError: If task doesn't complete within timeout
            KlingAPIError: If task fails
        """
        import asyncio

        start_time = time.time()

        while True:
            task = await get_task_func(task_id)

            if task.task_status == "succeed":
                return task
            elif task.task_status == "failed":
                raise KlingAPIError(
                    message=task.task_status_msg or "Task failed",
                    code=-1,
                    request_id="",
                )

            # Check timeout
            elapsed = time.time() - start_time
            if elapsed >= timeout:
                raise KlingTimeoutError(
                    f"Task {task_id} did not complete within {timeout} seconds"
                )

            # Wait before next poll
            await asyncio.sleep(poll_interval)

    def close(self):
        """Close HTTP clients."""
        self._client.close()

    async def close_async(self):
        """Close async HTTP client."""
        await self._async_client.aclose()

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
