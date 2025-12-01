"""Video generation Pydantic models."""

from typing import Optional, List, Union
from pydantic import BaseModel, Field
from kling.models.common import (
    ModelName,
    VideoMode,
    AspectRatio,
    VideoDuration,
    CameraControl,
)


class DynamicMaskTrajectory(BaseModel):
    """Trajectory point for dynamic mask."""

    x: int = Field(..., description="X-coordinate")
    y: int = Field(..., description="Y-coordinate")


class DynamicMask(BaseModel):
    """Dynamic brush configuration."""

    mask: str = Field(..., description="Mask image (Base64 or URL)")
    trajectories: List[DynamicMaskTrajectory] = Field(
        ...,
        min_length=2,
        max_length=77,
        description="Motion trajectory coordinates",
    )


class ImageInput(BaseModel):
    """Image input for multi-image to video."""

    image: str = Field(..., description="Image URL or Base64")


class TextToVideoRequest(BaseModel):
    """Text to video request parameters."""

    model_name: Optional[ModelName] = Field("kling-v1", description="Model version")
    prompt: str = Field(..., max_length=2500, description="Positive text prompt")
    negative_prompt: Optional[str] = Field(None, max_length=2500, description="Negative prompt")
    cfg_scale: Optional[float] = Field(0.5, ge=0, le=1, description="CFG scale")
    mode: Optional[VideoMode] = Field("std", description="Video generation mode")
    camera_control: Optional[CameraControl] = Field(None, description="Camera control")
    aspect_ratio: Optional[AspectRatio] = Field("16:9", description="Aspect ratio")
    duration: Optional[VideoDuration] = Field("5", description="Video duration in seconds")
    callback_url: Optional[str] = Field(None, description="Callback URL")
    external_task_id: Optional[str] = Field(None, description="External task ID")


class ImageToVideoRequest(BaseModel):
    """Image to video request parameters."""

    model_name: Optional[ModelName] = Field("kling-v1", description="Model version")
    image: Optional[str] = Field(None, description="Reference image (Base64 or URL)")
    image_tail: Optional[str] = Field(None, description="End frame image (Base64 or URL)")
    prompt: Optional[str] = Field(None, max_length=2500, description="Positive text prompt")
    negative_prompt: Optional[str] = Field(None, max_length=2500, description="Negative prompt")
    cfg_scale: Optional[float] = Field(0.5, ge=0, le=1, description="CFG scale")
    mode: Optional[VideoMode] = Field("std", description="Video generation mode")
    static_mask: Optional[str] = Field(None, description="Static mask image")
    dynamic_masks: Optional[List[DynamicMask]] = Field(
        None,
        max_length=6,
        description="Dynamic brush configurations",
    )
    camera_control: Optional[CameraControl] = Field(None, description="Camera control")
    duration: Optional[VideoDuration] = Field("5", description="Video duration in seconds")
    callback_url: Optional[str] = Field(None, description="Callback URL")
    external_task_id: Optional[str] = Field(None, description="External task ID")


class MultiImageToVideoRequest(BaseModel):
    """Multi-image to video request parameters (Elements)."""

    model_name: Optional[ModelName] = Field("kling-v1-6", description="Model version")
    image_list: List[ImageInput] = Field(
        ...,
        min_length=1,
        max_length=4,
        description="Reference images",
    )
    prompt: str = Field(..., max_length=2500, description="Positive text prompt")
    negative_prompt: Optional[str] = Field(None, max_length=2500, description="Negative prompt")
    mode: Optional[VideoMode] = Field("std", description="Video generation mode")
    duration: Optional[VideoDuration] = Field("5", description="Video duration in seconds")
    aspect_ratio: Optional[AspectRatio] = Field("16:9", description="Aspect ratio")
    callback_url: Optional[str] = Field(None, description="Callback URL")
    external_task_id: Optional[str] = Field(None, description="External task ID")


class VideoExtensionRequest(BaseModel):
    """Video extension request parameters."""

    video_id: str = Field(..., description="Video ID to extend")
    prompt: Optional[str] = Field(None, max_length=2500, description="Text prompt")
    negative_prompt: Optional[str] = Field(None, max_length=2500, description="Negative prompt")
    cfg_scale: Optional[float] = Field(0.5, ge=0, le=1, description="CFG scale")
    callback_url: Optional[str] = Field(None, description="Callback URL")
