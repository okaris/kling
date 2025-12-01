"""Audio generation Pydantic models."""

from typing import Optional, Literal
from pydantic import BaseModel, Field


class TextToAudioRequest(BaseModel):
    """Text to audio request parameters."""

    prompt: str = Field(..., max_length=200, description="Text prompt")
    duration: float = Field(..., ge=3.0, le=10.0, description="Duration in seconds")
    external_task_id: Optional[str] = Field(None, description="External task ID")
    callback_url: Optional[str] = Field(None, description="Callback URL")


class VideoToAudioRequest(BaseModel):
    """Video to audio request parameters."""

    video_id: Optional[str] = Field(None, description="Video ID from Kling AI")
    video_url: Optional[str] = Field(None, description="Video URL")
    sound_effect_prompt: Optional[str] = Field(
        None, max_length=200, description="Sound effect prompt"
    )
    bgm_prompt: Optional[str] = Field(None, max_length=200, description="BGM prompt")
    asmr_mode: Optional[bool] = Field(False, description="Enable ASMR mode")
    external_task_id: Optional[str] = Field(None, description="External task ID")
    callback_url: Optional[str] = Field(None, description="Callback URL")


VoiceLanguage = Literal["zh", "en"]


class TTSRequest(BaseModel):
    """Text-to-speech request parameters."""

    text: str = Field(..., max_length=1000, description="Text content")
    voice_id: str = Field(..., description="Voice ID")
    voice_language: VoiceLanguage = Field(..., description="Voice language")
    voice_speed: Optional[float] = Field(
        1.0, ge=0.8, le=2.0, description="Speech rate"
    )
