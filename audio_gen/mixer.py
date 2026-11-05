"""Montagem do MP3 final com pydub (ffmpeg) ou concat binário."""

from __future__ import annotations

import shutil
from pathlib import Path

from pydub import AudioSegment


def _ffmpeg_exe() -> str | None:
    found = shutil.which("ffmpeg") or shutil.which("avconv")
    if found:
        return found
    try:
        import imageio_ffmpeg
    except ImportError:
        return None
    return imageio_ffmpeg.get_ffmpeg_exe()


def _has_ffmpeg() -> bool:
    exe = _ffmpeg_exe()
    if not exe:
        return False
    AudioSegment.converter = exe
    return True


def _load_mp3(path: Path) -> AudioSegment:
    # codec força o decode sem ffprobe (o binário do imageio só traz o ffmpeg)
    return AudioSegment.from_file(path, format="mp3", codec="mp3")


def merge_mp3s(
    paths: list[Path],
    output_path: Path,
    *,
    pause_ms: int = 600,
    export_bitrate: str = "192k",
) -> Path:
    """Une vários MP3 com silêncio entre os segmentos."""
    if not paths:
        raise ValueError("Nenhum áudio para unir.")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if _has_ffmpeg():
        silence = AudioSegment.silent(duration=max(0, pause_ms))
        combined = AudioSegment.empty()
        for i, path in enumerate(paths):
            clip = _load_mp3(path)
            combined += clip
            if i < len(paths) - 1 and pause_ms > 0:
                combined += silence
        combined.export(output_path, format="mp3", bitrate=export_bitrate)
        return output_path

    # Fallback: MP3s da ElevenLabs (mesmo codec/bitrate) concatenam bem.
    # Sem ffmpeg não dá para inserir silêncio — os trechos ficam colados.
    print(
        "Aviso: ffmpeg não encontrado — unindo MP3 por concatenação direta "
        "(sem pausas). Instale ffmpeg para pausas e mixagem completa."
    )
    with output_path.open("wb") as out:
        for path in paths:
            out.write(Path(path).read_bytes())
    return output_path


def underscore(
    speech_path: Path,
    music_path: Path,
    output_path: Path,
    *,
    music_db: float = -18.0,
    export_bitrate: str = "192k",
) -> Path:
    """Coloca uma trilha instrumental por baixo da fala, em volume baixo."""
    if not _has_ffmpeg():
        raise RuntimeError(
            "ffmpeg é necessário para mixar a trilha por baixo da fala."
        )

    speech = _load_mp3(speech_path)
    music = _load_mp3(music_path) + music_db
    if len(music) < len(speech):
        repeats = (len(speech) // max(len(music), 1)) + 1
        music = music * repeats
    music = music[: len(speech)].fade_in(700).fade_out(1400)
    mixed = speech.overlay(music)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    mixed.export(output_path, format="mp3", bitrate=export_bitrate)
    return output_path
