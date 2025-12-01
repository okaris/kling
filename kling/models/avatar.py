"""Avatar and Lip-Sync Pydantic models."""

from typing import Optional, List, Literal
from pydantic import BaseModel, Field
from kling.models.common import VideoMode


class AvatarRequest(BaseModel):
    """Avatar generation request parameters."""

    image: str = Field(..., description="Avatar reference image (Base64 or URL)")
    audio_id: Optional[str] = Field(None, description="Audio ID from TTS API")
    sound_file: Optional[str] = Field(None, description="Sound file (Base64 or URL)")
    prompt: Optional[str] = Field(None, max_length=2500, description="Text prompt")
    mode: Optional[VideoMode] = Field("std", description="Video generation mode")
    callback_url: Optional[str] = Field(None, description="Callback URL")
    external_task_id: Optional[str] = Field(None, description="External task ID")


class FaceData(BaseModel):
    """Face data from identify_face response."""

    face_id: str = Field(..., description="Face ID")
    face_image: str = Field(..., description="Face image URL")
    start_time: int = Field(..., description="Start time in ms")
    end_time: int = Field(..., description="End time in ms")


class IdentifyFaceResponse(BaseModel):
    """Response from identify_face endpoint."""

    session_id: str = Field(..., description="Session ID for lip-sync")
    face_data: List[FaceData] = Field(..., description="List of detected faces")


class FaceChoice(BaseModel):
    """Face choice configuration for lip-sync."""

    face_id: str = Field(..., description="Face ID from identify_face")
    audio_id: Optional[str] = Field(None, description="Audio ID from TTS")
    sound_file: Optional[str] = Field(None, description="Sound file (Base64 or URL)")
    sound_start_time: int = Field(..., description="Sound start time in ms")
    sound_end_time: int = Field(..., description="Sound end time in ms")
    sound_insert_time: int = Field(..., description="Sound insert time in ms")
    sound_volume: Optional[float] = Field(1.0, ge=0, le=2, description="Sound volume")
    original_audio_volume: Optional[float] = Field(
        1.0, ge=0, le=2, description="Original audio volume"
    )


class LipSyncRequest(BaseModel):
    """Lip-sync request parameters."""

    session_id: str = Field(..., description="Session ID from identify_face")
    face_choose: List[FaceChoice] = Field(
        ..., min_length=1, max_length=1, description="Face configurations"
    )
    callback_url: Optional[str] = Field(None, description="Callback URL")


class IdentifyFaceRequest(BaseModel):
    """Identify face request parameters."""

    video_id: Optional[str] = Field(None, description="Video ID from Kling AI")
    video_url: Optional[str] = Field(None, description="Video URL")
