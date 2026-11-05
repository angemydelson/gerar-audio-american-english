"""Cliente ElevenLabs TTS."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

from .models import VoiceProfile
from .voices import resolve_voice


def get_client(api_key: str | None = None) -> ElevenLabs:
    env_path = Path(__file__).resolve().parents[1] / ".env"
    load_dotenv(env_path, override=True)
    key = api_key or os.getenv("ELEVENLABS_API_KEY")
    if not key:
        raise RuntimeError(
            "Defina ELEVENLABS_API_KEY no .env ou passe api_key=..."
        )
    return ElevenLabs(api_key=key)


def synthesize_to_file(
    text: str,
    speaker: str,
    output_path: Path,
    *,
    cast: dict[str, VoiceProfile] | None = None,
    voice_overrides: dict | None = None,
    model_id: str = "eleven_turbo_v2_5",
    output_format: str = "mp3_44100_128",
    client: ElevenLabs | None = None,
) -> Path:
    """Gera um MP3 para um trecho (inglês americano)."""
    profile = resolve_voice(speaker, cast=cast, overrides=voice_overrides)
    eleven = client or get_client()
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    stream = eleven.text_to_speech.convert(
        voice_id=profile.voice_id,
        text=text,
        model_id=model_id,
        output_format=output_format,
        # turbo/flash v2.5: força inglês (vozes americanas no cast)
        language_code="en",
        voice_settings=VoiceSettings(
            stability=profile.stability,
            similarity_boost=profile.similarity_boost,
            style=profile.style,
            use_speaker_boost=profile.use_speaker_boost,
            speed=profile.speed,
        ),
    )

    try:
        with output_path.open("wb") as fh:
            for chunk in stream:
                if chunk:
                    fh.write(chunk)
    except Exception as exc:
        if output_path.exists() and output_path.stat().st_size == 0:
            output_path.unlink(missing_ok=True)
        message = str(exc)
        body = getattr(exc, "body", None)
        detail = ""
        if isinstance(body, dict):
            detail = str(body.get("detail", body))
        combined = f"{message} {detail}".lower()
        if "quota_exceeded" in combined:
            raise RuntimeError(
                "Cota ElevenLabs esgotada. Espere o reset ou use outra conta/plano."
            ) from exc
        if "detected_unusual_activity" in combined:
            raise RuntimeError(
                "Conta ElevenLabs bloqueada no Free Tier (unusual activity). "
                "Desative VPN/proxy, use outra conta, ou faça upgrade pago."
            ) from exc
        if "missing_permissions" in combined or "unauthorized" in combined:
            raise RuntimeError(
                "A API key não tem permissão text_to_speech. "
                "Atualize as permissions no painel ElevenLabs."
            ) from exc
        raise

    if output_path.stat().st_size == 0:
        output_path.unlink(missing_ok=True)
        raise RuntimeError(f"Áudio vazio gerado para {speaker!r}.")

    return output_path


def synthesize_sfx(
    prompt: str,
    output_path: Path,
    *,
    duration_seconds: float | None = 1.8,
    client: ElevenLabs | None = None,
) -> Path:
    """Gera um efeito sonoro curto (MP3) e retorna o caminho."""
    eleven = client or get_client()
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    kwargs = {
        "text": prompt,
        "output_format": "mp3_44100_128",
        "prompt_influence": 0.5,
    }
    if duration_seconds:
        kwargs["duration_seconds"] = max(0.5, min(8.0, float(duration_seconds)))

    stream = eleven.text_to_sound_effects.convert(**kwargs)
    try:
        with output_path.open("wb") as fh:
            for chunk in stream:
                if chunk:
                    fh.write(chunk)
    except Exception as exc:
        if output_path.exists() and output_path.stat().st_size == 0:
            output_path.unlink(missing_ok=True)
        raise RuntimeError(f"Falha ao gerar efeito sonoro: {exc}") from exc

    if not output_path.exists() or output_path.stat().st_size == 0:
        output_path.unlink(missing_ok=True)
        raise RuntimeError("Efeito sonoro vazio.")

    return output_path


def synthesize_music(
    prompt: str,
    output_path: Path,
    *,
    length_ms: int = 20000,
    client: ElevenLabs | None = None,
) -> Path:
    """Gera uma trilha instrumental curta, para ficar por baixo da fala."""
    eleven = client or get_client()
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    stream = eleven.music.compose(
        prompt=prompt,
        music_length_ms=max(3000, min(60000, int(length_ms))),
        force_instrumental=True,
        output_format="mp3_44100_128",
    )
    try:
        with output_path.open("wb") as fh:
            for chunk in stream:
                if chunk:
                    fh.write(chunk)
    except Exception as exc:
        if output_path.exists() and output_path.stat().st_size == 0:
            output_path.unlink(missing_ok=True)
        body = getattr(exc, "body", None)
        raise RuntimeError(f"Falha ao gerar trilha: {body or exc}") from exc

    if not output_path.exists() or output_path.stat().st_size == 0:
        output_path.unlink(missing_ok=True)
        raise RuntimeError("Trilha vazia.")

    return output_path
