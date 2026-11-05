#!/usr/bin/env python3
"""
Gera áudio com ElevenLabs a partir de um roteiro.

Exemplos:
  python generate_audio.py
  python generate_audio.py content/americans_abroad.json -o output/americans.mp3
  python generate_audio.py content/meu_dialogo.txt -o output/dialogo.mp3

Formatos de entrada:
  .json      → roteiro estruturado (recomendado)
  .txt/.dialogue → linhas "Speaker: texto"

Para novos formatos, implemente ScriptLoader em audio_gen/loaders.py.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from audio_gen.loaders import load_script
from audio_gen.pipeline import generate_script_audio


def filename_from_title(title: str) -> str:
    """Usa o título do roteiro/imagem como nome do MP3."""
    cleaned = re.sub(r'[<>:"/\\|?*]', "", title).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return f"{cleaned}.mp3"


def main() -> None:
    root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        description="Gera MP3 com vozes distintas por personagem (ElevenLabs + pydub)."
    )
    parser.add_argument(
        "source",
        nargs="?",
        default=str(root / "content" / "americans_abroad.json"),
        help="Arquivo de roteiro (.json, .txt, .dialogue)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Caminho do MP3 final (padrão: output/<título da imagem>.mp3)",
    )
    parser.add_argument(
        "--model",
        default="eleven_turbo_v2_5",
        help="Modelo ElevenLabs (padrão: eleven_turbo_v2_5 com inglês americano)",
    )
    parser.add_argument(
        "--no-keep-parts",
        action="store_true",
        help="Apaga os MP3 parciais após unir",
    )
    args = parser.parse_args()

    script = load_script(args.source)
    output = Path(args.output) if args.output else (
        root / "output" / filename_from_title(script.title)
    )

    result = generate_script_audio(
        script,
        output,
        model_id=args.model,
        keep_parts=not args.no_keep_parts,
    )
    print(f"Pronto: {result.resolve()}")


if __name__ == "__main__":
    main()
