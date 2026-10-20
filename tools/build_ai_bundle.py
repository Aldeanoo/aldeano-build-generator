#!/usr/bin/env python3
"""Build the single-file chat kit without dependencies."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import generator as g


def build_bundle():
    conversation = (ROOT / "instructions/conversation.es.md").read_text(encoding="utf-8")
    runtime = (ROOT / "instructions/runtime.md").read_text(encoding="utf-8")
    code = (ROOT / "generator.py").read_text(encoding="utf-8").rstrip() + "\n"
    architect = (ROOT / "architect.py").read_text(encoding="utf-8").rstrip() + "\n"
    example = {"schema": "aldeano-architecture/v1", "name": "posada_del_roble",
               "template": "medieval_inn", "theme": "medieval", "seed": 7,
               "features": ["garden", "balcony", "dormer", "chimney", "interior"]}
    from architect import build_architecture
    g.validate_build(build_architecture(example))
    return (
        conversation.rstrip() + "\n\n" + runtime.rstrip()
        + "\n\n## Catalogo completo\n\n" + ", ".join(g.MATERIALS)
        + "\n\n## Ejemplo valido completo\n\n```json\n"
        + json.dumps(example, ensure_ascii=False, separators=(",", ":"))
        + "\n```\n\n## architect.py - copiar este bloque sin cambios\n\n```python\n"
        + architect.rstrip()
        + "\n```\n\n## generator.py - copiar este bloque sin cambios\n\n```python\n"
        + code.rstrip() + "\n```\n\n"
        + f"Kit v{g.VERSION}. Fuente: {g.REPO}. Licencia MIT. "
        + "Copyright (c) 2026 Aldeanoo.\n"
        + "SHA-256 de generator.py: " + hashlib.sha256(code.encode("utf-8")).hexdigest() + "\n"
        + "SHA-256 de architect.py: " + hashlib.sha256(architect.encode("utf-8")).hexdigest() + "\n"
        + "Comienza ahora con las preguntas que falten; no des una explicacion "
        + "larga del funcionamiento del kit.\n"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    content = build_bundle()
    for filename in ("INICIO_IA.md", "INICIO_IA.txt"):
        path = ROOT / filename
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                raise SystemExit(f"{filename} no coincide: ejecuta tools/build_ai_bundle.py.")
        else:
            path.write_bytes(content.encode("utf-8"))
    print(f"Kit v{g.VERSION}: {len(content.encode('utf-8'))} bytes; "
          + ("verificado" if args.check else "generado"))


if __name__ == "__main__":
    main()
