from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class VoiceProfile:
    """Configuração de voz ElevenLabs para um personagem."""

    voice_id: str
    name: str
    description: str = ""
    # Estilo de performance (afeta expressividade no modelo multilingual/v2+)
    stability: float = 0.45
    similarity_boost: float = 0.80
    style: float = 0.35
    speed: float = 1.0
    use_speaker_boost: bool = True


@dataclass
class Segment:
    """Um bloco de fala (personagem ou narrador)."""

    speaker: str
    text: str
    label: str | None = None
    # Override opcional por segmento (ex.: outro voice_id só neste trecho)
    voice_overrides: dict[str, Any] = field(default_factory=dict)
    # Se preenchido, o segmento é um efeito sonoro (não é falado)
    sfx: str | None = None
    sfx_seconds: float | None = None


@dataclass
class Script:
    """Roteiro genérico — serve para entrevista, diálogo, podcast, etc."""

    id: str
    title: str
    segments: list[Segment]
    language: str = "en"
    pause_ms_between_segments: int = 600
    include_intro: bool = False
    intro_text: str | None = None
    intro_speaker: str = "narrator"
    # Se True, fala o label (nome/idade/país) antes do depoimento
    speak_labels: bool = True
    # Trilha instrumental por baixo da fala (prompt para a API de música)
    music: str | None = None
    music_db: float = -18.0
    # Mapa speaker -> VoiceProfile (pode vir do JSON ou do registry)
    voices: dict[str, VoiceProfile] = field(default_factory=dict)

    def iter_speakable(self) -> list[Segment]:
        items: list[Segment] = []
        if self.include_intro and self.intro_text:
            items.append(
                Segment(
                    speaker=self.intro_speaker,
                    text=self.intro_text,
                    label=self.title,
                )
            )
        items.extend(self.segments)
        return items
