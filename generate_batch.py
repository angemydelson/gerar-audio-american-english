#!/usr/bin/env python3
"""Gera vários roteiros de content/ de uma vez."""

from __future__ import annotations

import sys
from pathlib import Path

from generate_audio import filename_from_title
from audio_gen.loaders import load_script
from audio_gen.pipeline import generate_script_audio

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
OUTPUT = ROOT / "output"

# Ordem dos novos áudios (além do Americans Abroad já gerado)
BATCH = [
    "things_i_didnt_know.json",
    "my_dreams_stef.json",
    "written_in_the_cards.json",
    "travers_murder.json",
    "life_before_internet.json",
]


def main() -> None:
    files = [CONTENT / name for name in (sys.argv[1:] or BATCH)]
    for path in files:
        if not path.exists():
            print(f"Pulado (não existe): {path}")
            continue
        script = load_script(path)
        out = OUTPUT / filename_from_title(script.title)
        print(f"\n=== {script.title} ===")
        generate_script_audio(script, out, keep_parts=True)
        print(f"OK → {out}")


if __name__ == "__main__":
    main()
