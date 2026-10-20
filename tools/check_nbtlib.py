"""Optional independent reader over the same manifest as check_prismarine.cjs."""
import gzip
import io
import json
from pathlib import Path
import sys

import nbtlib


def main():
    manifest = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    results = []
    for item in manifest:
        path = Path(item["file"])
        blob = path.read_bytes()
        raw = gzip.decompress(blob) if item["format"] == "big" else blob
        stream = io.BytesIO(raw)
        root = nbtlib.File.parse(stream, byteorder=item["format"])
        assert stream.read() == b"", "NBT must be consumed entirely"
        assert root.unpack() == json.loads(Path(item["expected"]).read_text(encoding="utf-8"))
        rewritten = io.BytesIO()
        root.write(rewritten, byteorder=item["format"])
        assert rewritten.getvalue() == raw, "Independent binary roundtrip"
        results.append({"file": str(path), "bytes": len(blob), "passed": True})
    print(json.dumps({"reader": "nbtlib", "version": nbtlib.__version__,
                      "checked": len(results), "files": results}, indent=2))


if __name__ == "__main__":
    main()
