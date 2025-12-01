"""Video Effects Pydantic models."""

from typing import Optional, Union, Dict, Any, List
from pydantic import BaseModel, Field
from kling.models.common import ModelName, VideoMode


# All available effect scenes
EffectScene = str  # Too many to enumerate, accept any string


class SingleImageEffectInput(BaseModel):
    """Input for single-image effects."""

    image: str = Field(..., description="Reference image (Base64 or URL)")
    duration: str = Field(..., description="Video duration in seconds")


class DualCharacterEffectInput(BaseModel):
    """Input for dual-character effects."""

    model_name: Optional[ModelName] = Field("kling-v1", description="Model version")
    mode: Optional[VideoMode] = Field("std", description="Video generation mode")
    images: List[str] = Field(
        ..., min_length=2, max_length=2, description="Two images (left, right)"
    )
    duration: str = Field(..., description="Video duration in seconds")


class VideoEffectsRequest(BaseModel):
    """Video effects request parameters."""

    effect_scene: str = Field(..., description="Effect scene name")
    input: Union[SingleImageEffectInput, DualCharacterEffectInput, Dict[str, Any]] = Field(
        ..., description="Effect input parameters"
    )
    callback_url: Optional[str] = Field(None, description="Callback URL")
    external_task_id: Optional[str] = Field(None, description="External task ID")
