"""Loaders de entrada — fácil adicionar novos formatos (md, csv, yaml...)."""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from .models import Script, Segment, VoiceProfile
from .voices import DEFAULT_CAST


class ScriptLoader(ABC):
    """Contrato para qualquer fonte de roteiro."""

    @abstractmethod
    def load(self, source: str | Path) -> Script:
        raise NotImplementedError


def _parse_voice_profile(data: dict[str, Any]) -> VoiceProfile:
    return VoiceProfile(
        voice_id=data["voice_id"],
        name=data.get("name", data["voice_id"]),
        description=data.get("description", ""),
        stability=float(data.get("stability", 0.45)),
        similarity_boost=float(data.get("similarity_boost", 0.80)),
        style=float(data.get("style", 0.35)),
        speed=float(data.get("speed", 1.0)),
        use_speaker_boost=bool(data.get("use_speaker_boost", True)),
    )


def script_from_dict(data: dict[str, Any]) -> Script:
    """Converte um dict normalizado em Script (reutilizável por qualquer loader)."""
    cast = dict(DEFAULT_CAST)
    for speaker, voice_data in (data.get("voices") or {}).items():
        cast[speaker.lower()] = _parse_voice_profile(voice_data)

    segments = []
    for item in data["segments"]:
        sfx = (item.get("sfx") or "").strip() or None
        segments.append(
            Segment(
                speaker=(item.get("speaker") or ("sfx" if sfx else "")).strip(),
                text=(item.get("text") or "").strip(),
                label=item.get("label"),
                voice_overrides=item.get("voice_overrides") or {},
                sfx=sfx,
                sfx_seconds=item.get("sfx_seconds"),
            )
        )

    return Script(
        id=data.get("id") or "script",
        title=data.get("title") or "Untitled",
        language=data.get("language", "en"),
        pause_ms_between_segments=int(data.get("pause_ms_between_segments", 600)),
        include_intro=bool(data.get("include_intro", False)),
        intro_text=data.get("intro_text"),
        intro_speaker=data.get("intro_speaker", "narrator"),
        speak_labels=bool(data.get("speak_labels", True)),
        music=(data.get("music") or "").strip() or None,
        music_db=float(data.get("music_db", -18)),
        segments=segments,
        voices=cast,
    )


class JsonScriptLoader(ScriptLoader):
    """
    Formato esperado (exemplo em content/americans_abroad.json):

    {
      "id": "...",
      "title": "...",
      "include_intro": true,
      "intro_text": "...",
      "pause_ms_between_segments": 650,
      "segments": [
        {"speaker": "amy", "label": "...", "text": "..."}
      ],
      "voices": {                 // opcional — sobrescreve o cast padrão
        "amy": {"voice_id": "...", "stability": 0.3, "style": 0.6}
      }
    }
    """

    def load(self, source: str | Path) -> Script:
        path = Path(source)
        data = json.loads(path.read_text(encoding="utf-8"))
        return script_from_dict(data)


class PlainDialogueLoader(ScriptLoader):
    """
    Texto simples no formato:

        Narrator: Hello everyone.
        Amy: I love Thailand!

    Útil para rascunhos rápidos / outros tipos de áudio.
    """

    def load(self, source: str | Path) -> Script:
        path = Path(source)
        segments: list[Segment] = []
        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if ":" not in line:
                raise ValueError(
                    f"Linha inválida (use 'Speaker: texto'): {line!r}"
                )
            speaker, text = line.split(":", 1)
            segments.append(Segment(speaker=speaker.strip(), text=text.strip()))

        return Script(
            id=path.stem,
            title=path.stem.replace("_", " ").title(),
            segments=segments,
            voices=dict(DEFAULT_CAST),
        )


LOADERS: dict[str, ScriptLoader] = {
    ".json": JsonScriptLoader(),
    ".txt": PlainDialogueLoader(),
    ".dialogue": PlainDialogueLoader(),
}


def load_script(source: str | Path) -> Script:
    path = Path(source)
    if not path.exists():
        raise FileNotFoundError(path)
    loader = LOADERS.get(path.suffix.lower())
    if loader is None:
        supported = ", ".join(sorted(LOADERS))
        raise ValueError(
            f"Extensão {path.suffix!r} não suportada. Use: {supported}. "
            "Para novos formatos, implemente ScriptLoader em audio_gen/loaders.py."
        )
    return loader.load(path)
