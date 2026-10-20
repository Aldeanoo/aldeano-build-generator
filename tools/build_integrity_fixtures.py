"""Create cross-reader fixtures in ignored .cache, including a published baseline."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import generator as g


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", help="Also check these previously published Git files, e.g. v0.2.0")
    args = parser.parse_args()
    folder = ROOT / ".cache/integrity"
    folder.mkdir(parents=True, exist_ok=True)
    manifest = []

    def add(label, extension, blob):
        path = folder / (label + "." + extension)
        expected = folder / (label + "." + extension + ".json")
        root = g.read_structure(blob, extension)
        path.write_bytes(blob)
        expected.write_text(json.dumps(root), encoding="utf-8")
        manifest.append({"file": str(path), "expected": str(expected),
                         "format": "big" if extension == "nbt" else "little"})

    for source in sorted((ROOT / "examples").glob("*.json")):
        build = g.parse_build(source.read_text(encoding="utf-8"))
        outputs, report = g.generate(build)
        name = report["name"]
        add(name, "mcstructure", outputs[name + ".mcstructure"])
        for profile in g.JAVA_PROFILES:
            outputs, _ = g.generate(build, delivery="nbt", java_profile=profile)
            add(name + "-" + profile, "nbt", outputs[name + ".nbt"])
        if args.baseline:
            for ext in ("nbt", "mcstructure"):
                git_path = f"samples/{name}/{name}.{ext}"
                blob = subprocess.run(["git", "show", f"{args.baseline}:{git_path}"],
                                      cwd=ROOT, capture_output=True, check=True).stdout
                add(name + "-baseline", ext, blob)
    path = folder / "manifest.json"
    path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps({"fixtures": len(manifest), "manifest": str(path)}))


if __name__ == "__main__":
    main()
