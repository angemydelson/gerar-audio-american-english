"""Pipeline para gerar áudios com ElevenLabs a partir de roteiros tipados."""

from .models import Script, Segment, VoiceProfile
from .pipeline import generate_script_audio

__all__ = [
    "Script",
    "Segment",
    "VoiceProfile",
    "generate_script_audio",
]
