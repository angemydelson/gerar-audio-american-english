"""Orquestra: load → TTS por segmento → merge MP3."""

from __future__ import annotations

import shutil
from pathlib import Path

from .loaders import load_script
from .mixer import merge_mp3s, underscore
from .models import Script
from .tts import get_client, synthesize_music, synthesize_to_file


def generate_script_audio(
    source: str | Path | Script,
    output_path: str | Path,
    *,
    work_dir: str | Path | None = None,
    model_id: str = "eleven_turbo_v2_5",
    keep_parts: bool = True,
) -> Path:
    """
    Gera um MP3 único a partir de um arquivo de roteiro (.json / .txt)
    ou de um objeto Script já montado.
    """
    script = source if isinstance(source, Script) else load_script(source)
    out = Path(output_path)
    parts_dir = Path(work_dir) if work_dir else out.parent / f".parts_{script.id}"
    parts_dir.mkdir(parents=True, exist_ok=True)

    client = get_client()
    part_paths: list[Path] = []
    speakable = script.iter_speakable()

    for index, segment in enumerate(speakable, start=1):
        safe_speaker = segment.speaker.lower().replace(" ", "_")
        part_path = parts_dir / f"{index:02d}_{safe_speaker}.mp3"
        if segment.sfx and not segment.text:
            print(f"[{index}/{len(speakable)}] som avulso ignorado (a trilha vai por baixo da fala)")
            continue

        spoken = (
            _spoken_text(segment.label, segment.text)
            if script.speak_labels
            else segment.text
        )
        if part_path.exists() and part_path.stat().st_size > 0:
            print(f"[{index}/{len(speakable)}] {segment.speaker}: (já existe, pulando)")
        else:
            print(f"[{index}/{len(speakable)}] {segment.speaker}: {segment.text[:60]}...")
            synthesize_to_file(
                text=spoken,
                speaker=segment.speaker,
                output_path=part_path,
                cast=script.voices,
                voice_overrides=segment.voice_overrides or None,
                model_id=model_id,
                client=client,
            )
        part_paths.append(part_path)

    print(f"Unindo {len(part_paths)} partes → {out}")
    speech_out = out
    if script.music:
        speech_out = parts_dir / "_speech.mp3"
    merge_mp3s(
        part_paths,
        speech_out,
        pause_ms=script.pause_ms_between_segments,
    )
    if script.music:
        music_path = parts_dir / "_music.mp3"
        try:
            if not (music_path.exists() and music_path.stat().st_size > 0):
                print("Gerando trilha instrumental...")
                synthesize_music(script.music, music_path, client=client)
            print("Mixando trilha por baixo da fala...")
            underscore(speech_out, music_path, out, music_db=script.music_db)
        except RuntimeError as exc:
            print(f"Trilha não mixada ({exc}). Mantendo só a fala.")
            if speech_out != out:
                shutil.copyfile(speech_out, out)

    if not keep_parts:
        for path in part_paths:
            path.unlink(missing_ok=True)
        try:
            parts_dir.rmdir()
        except OSError:
            pass

    return out


def _spoken_text(label: str | None, text: str) -> str:
    """Opcionalmente fala o rótulo (nome/idade/país) antes do depoimento."""
    if label:
        return f"{label} {text}"
    return text
