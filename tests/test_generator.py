import copy
import gzip
import hashlib
import importlib.util
import io
import json
import re
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

import jsonschema
import nbtlib

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import generator as g


def fixture():
    return json.loads((ROOT / "tests/fixtures/axis.build.json").read_text(encoding="utf-8"))


def parsed(blob, little=False, zipped=False):
    if zipped:
        blob = gzip.decompress(blob)
    stream = io.BytesIO(blob)
    result = nbtlib.File.parse(stream, byteorder="little" if little else "big")
    assert stream.read() == b"", "Trailing bytes"
    return result


class ValidationTests(unittest.TestCase):
    def test_examples_match_schema_and_runtime(self):
        schema = json.loads((ROOT / "schema/aldeano-build-v1.schema.json").read_text())
        jsonschema.Draft202012Validator.check_schema(schema)
        for source in sorted((ROOT / "examples").glob("*.build.json")):
            with self.subTest(source=source.name):
                data = g.parse_build(source.read_text())
                jsonschema.validate(data, schema)
                self.assertEqual(g.validate_build(data), data)

    def test_duplicate_json_keys_rejected(self):
        with self.assertRaises(g.BuildError):
            g.parse_build('{"name":"a","name":"b"}')

    def test_nonfinite_numbers_rejected(self):
        for word in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(word=word), self.assertRaises(g.BuildError):
                g.parse_build('{"n":' + word + '}')

    def test_complete_markdown_wrapper(self):
        data = fixture()
        for fence in ("```", "~~~"):
            self.assertEqual(g.parse_build(fence + "json\n" + json.dumps(data) + "\n" + fence), data)

    def test_prose_and_mixed_fences_rejected(self):
        for text in ('Here is JSON: {}', '```json\n{}\n~~~', '```json\n{}'):
            with self.subTest(text=text), self.assertRaises(g.BuildError):
                g.parse_build(text)

    def test_input_size_and_deep_nesting(self):
        for text in (" " * (g.MAX_BYTES + 1), "[" * 1500 + "]" * 1500):
            with self.assertRaises(g.BuildError):
                g.parse_build(text)

    def test_invalid_shapes(self):
        cases = []
        for key, value in (("name", "../bad"), ("name", "bad\n"), ("size", [True, 2, 4]),
                           ("size", [3.0, 2, 4]), ("size", [0, 2, 4]),
                           ("size", [33, 2, 4]), ("ops", []),
                           ("schema", "unknown"), ("palette", {"a": "command_block"})):
            item = fixture()
            item[key] = value
            cases.append(item)
        item = fixture(); item["surprise"] = "not allowed"; cases.append(item)
        item = fixture(); item["ops"][0]["nbt"] = {}; cases.append(item)
        item = fixture(); item["ops"][0]["block"] = "unknown"; cases.append(item)
        item = fixture(); item["ops"][0]["at"] = [3, 0, 0]; cases.append(item)
        for item in cases:
            with self.subTest(item=item), self.assertRaises(g.BuildError):
                g.validate_build(item)

    def test_reversed_fill_rejected(self):
        item = fixture()
        item["ops"] = [{"op": "fill", "from": [2, 0, 0], "to": [1, 0, 0], "block": "stone"}]
        with self.assertRaises(g.BuildError):
            g.validate_build(item)

    def test_write_budget_accounts_for_overlaps(self):
        item = fixture()
        item["size"] = [32, 32, 32]
        item["ops"] = [{"op": "fill", "from": [0, 0, 0], "to": [31, 31, 31],
                        "block": "stone"}] * 123
        with self.assertRaisesRegex(g.BuildError, "presupuesto"):
            g.validate_build(item)

    def test_large_mode_explicit(self):
        item = fixture()
        item["size"] = [48, 1, 1]
        item["ops"] = [{"op": "set", "at": [47, 0, 0], "block": "stone"}]
        with self.assertRaises(g.BuildError):
            g.validate_build(item)
        self.assertEqual(g.validate_build(item, 48), item)


class GeometryTests(unittest.TestCase):
    def test_inclusive_fill_and_last_write(self):
        item = fixture()
        item["size"] = [2, 2, 2]
        item["ops"] = [
            {"op": "fill", "from": [0, 0, 0], "to": [1, 1, 1], "block": "stone"},
            {"op": "set", "at": [1, 1, 1], "block": "air"},
        ]
        volume = g.compile_volume(g.validate_build(item))
        values = [volume["palette"][n] for n in volume["cells"]]
        self.assertEqual(values.count("stone"), 7)
        self.assertEqual(values.count("air"), 1)

    def test_asymmetric_positions(self):
        volume = g.compile_volume(fixture())
        expected = {(0, 0, 0): "stone", (2, 1, 3): "gold_block", (1, 0, 2): "bricks",
                    (0, 1, 0): "sea_lantern", (1, 1, 1): "air"}
        actual = {tuple(pos): volume["palette"][state] for pos, state in g.positions(volume)}
        self.assertEqual(actual, expected)
        self.assertEqual(volume["cells"].count(-1), 19)

    def test_air_is_not_omission(self):
        outputs, report = g.generate(fixture())
        self.assertEqual(report["explicit_air"], 1)
        self.assertEqual(report["omitted_cells"], 19)
        self.assertEqual(report["placed_blocks"], 4)
        self.assertNotIn("air:", outputs["materiales.txt"].decode())


class BinaryTests(unittest.TestCase):
    def setUp(self):
        self.build = fixture()
        self.volume = g.compile_volume(self.build)

    def test_bedrock_with_independent_reader(self):
        root = parsed(g.export_mcstructure(self.volume), little=True)
        self.assertEqual(root["format_version"], 1)
        self.assertIsInstance(root["size"], nbtlib.List[nbtlib.Int])
        self.assertEqual(list(map(int, root["size"])), [3, 2, 4])
        layers = root["structure"]["block_indices"]
        self.assertIsInstance(layers, nbtlib.List[nbtlib.List])
        self.assertEqual([list(map(int, row)) for row in layers],
                         [self.volume["cells"], [-1] * 24])
        palette = root["structure"]["palette"]["default"]["block_palette"]
        by_name = {str(entry["name"]): entry for entry in palette}
        self.assertIn("minecraft:brick_block", by_name)
        for entry in palette:
            self.assertIsInstance(entry["version"], nbtlib.Int)
            self.assertEqual(entry["version"], g.BEDROCK_VERSION)

    def test_both_java_profiles_with_independent_reader(self):
        for profile in g.JAVA_PROFILES:
            with self.subTest(profile=profile):
                root = parsed(g.export_java_structure(self.volume, profile), zipped=True)
                key = "id" if profile == "java-26.3" else "Name"
                self.assertEqual(root["DataVersion"], g.JAVA_PROFILES[profile]["data_version"])
                blocks = {tuple(map(int, b["pos"])): str(root["palette"][int(b["state"])][key])
                          for b in root["blocks"]}
                self.assertEqual(len(blocks), 5)
                self.assertEqual(blocks[(2, 1, 3)], "minecraft:gold_block")
                self.assertEqual(blocks[(1, 0, 2)], "minecraft:bricks")
                self.assertEqual(blocks[(1, 1, 1)], "minecraft:air")
                self.assertNotIn((2, 0, 0), blocks)
                self.assertIsInstance(root["entities"], nbtlib.List[nbtlib.Compound])

    def test_all_materials_and_typed_quartz_states(self):
        item = fixture()
        item["size"] = [17, 2, 4]
        all_entries = []
        materials = list(g.MATERIALS)
        for start in range(0, len(materials), 64):
            batch = materials[start:start+64]
            item["palette"] = {m: m for m in batch}
            item["ops"] = [{"op": "set", "at": [i // 4, 0, i % 4], "block": m}
                           for i, m in enumerate(batch)]
            for op in item["ops"]:
                if op["block"] == "spruce_door_lower": op["at"] = [16,0,0]
                if op["block"] == "spruce_door_upper": op["at"] = [16,1,0]
            outputs, _ = g.generate(item)
            root = parsed(outputs["axis_fixture.mcstructure"], little=True)
            entries = root["structure"]["palette"]["default"]["block_palette"]
            self.assertEqual(len(entries), len(batch))
            all_entries.extend(entries)
        quartz = next(x for x in all_entries if x["name"] == "minecraft:quartz_block")
        self.assertIsInstance(quartz["states"]["pillar_axis"], nbtlib.String)
        self.assertEqual(quartz["states"]["pillar_axis"], "y")

    def test_tampered_geometry_fails_validation(self):
        outputs, _ = g.generate(self.build)
        wrong = copy.deepcopy(self.volume)
        wrong["cells"][0] = -1
        outputs["axis_fixture.mcstructure"] = g.export_mcstructure(wrong)
        with self.assertRaises(g.BuildError):
            g.validate_outputs(outputs, self.volume, self.build["name"], "both", "java-26.3")

    def test_truncation_and_trailing_bytes_rejected(self):
        blob = g.export_mcstructure(self.volume)
        for altered in (blob[:-1], blob + b"x"):
            with self.assertRaises(g.BuildError):
                g.read_nbt(altered, little=True)

    def test_maximum_volume(self):
        item = fixture()
        item["size"] = [48, 48, 48]
        item["ops"] = [{"op": "fill", "from": [0, 0, 0], "to": [47, 47, 47], "block": "stone"}]
        outputs, report = g.generate(item, max_size=48)
        self.assertEqual(report["placed_blocks"], 110592)
        root = parsed(outputs["axis_fixture.nbt"], zipped=True)
        self.assertEqual(len(root["blocks"]), 110592)


class PackageTests(unittest.TestCase):
    def test_packages_are_ready_to_install(self):
        for profile in g.JAVA_PROFILES:
            outputs, _ = g.generate(fixture(), java_profile=profile)
            with zipfile.ZipFile(io.BytesIO(outputs["axis_fixture.datapack.zip"])) as archive:
                self.assertEqual(set(archive.namelist()),
                                 {"pack.mcmeta", "data/aldeano/structure/axis_fixture.nbt"})
                meta = json.loads(archive.read("pack.mcmeta"))["pack"]
                if profile == "java-26.3":
                    self.assertEqual(meta["min_format"], [121, 0])
                    self.assertEqual(meta["max_format"], [121, 0])
                else:
                    self.assertEqual(meta["pack_format"], 48)
            with zipfile.ZipFile(io.BytesIO(outputs["axis_fixture.mcpack"])) as archive:
                meta = json.loads(archive.read("manifest.json"))
                self.assertNotEqual(meta["header"]["uuid"], meta["modules"][0]["uuid"])
                self.assertEqual(meta["header"]["min_engine_version"], [1, 26, 30])
                self.assertEqual(meta["modules"][0]["type"], "data")

    def test_pack_update_keeps_identity_and_changes_version(self):
        ids = []
        for version in ((1, 0, 0), (1, 0, 1)):
            outputs, _ = g.generate(fixture(), pack_version=version)
            with zipfile.ZipFile(io.BytesIO(outputs["axis_fixture.mcpack"])) as archive:
                meta = json.loads(archive.read("manifest.json"))
                ids.append(meta["header"]["uuid"])
                self.assertEqual(meta["header"]["version"], list(version))
        self.assertEqual(ids[0], ids[1])

    def test_reproducible_outputs_and_integrity(self):
        first, report = g.generate(fixture())
        second, _ = g.generate(fixture())
        self.assertEqual(first, second)
        for name, sha in report["sha256"].items():
            self.assertEqual(hashlib.sha256(first[name]).hexdigest(), sha)
        self.assertFalse(report["validation"]["minecraft_tested"])

    def test_single_edition_does_not_include_other_edition(self):
        for edition, forbidden in (("java", ".mcpack"), ("bedrock", ".datapack.zip")):
            outputs, _ = g.generate(fixture(), edition)
            self.assertFalse(any(n.endswith(forbidden) for n in outputs))


class PortableKitTests(unittest.TestCase):
    def test_bundle_matches_and_runs_without_repository(self):
        spec = importlib.util.spec_from_file_location("bundle", ROOT / "tools/build_ai_bundle.py")
        builder = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(builder)
        expected = builder.build_bundle()
        self.assertEqual((ROOT / "INICIO_IA.md").read_text(encoding="utf-8"), expected)
        self.assertEqual((ROOT / "INICIO_IA.txt").read_text(encoding="utf-8"), expected)
        def extract(filename):
            pattern = r"(?ms)^## " + re.escape(filename) + r" -[^\n]*\n+```python\n(.*?)^```[ \t]*$"
            return re.search(pattern, expected).group(1).rstrip()
        code = extract("generator.py")
        architect_code = extract("architect.py")
        # Source has no fences at the beginning of a line inside its literal strings.
        self.assertEqual(code, (ROOT / "generator.py").read_text(encoding="utf-8").rstrip())
        with tempfile.TemporaryDirectory() as folder:
            work = Path(folder)
            (work / "generator.py").write_text(code, encoding="utf-8")
            (work / "architect.py").write_text(architect_code, encoding="utf-8")
            (work / "design.json").write_text(json.dumps(fixture()), encoding="utf-8")
            run = subprocess.run([sys.executable, "-S", "generator.py", "design.json"],
                                 cwd=work, capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertTrue((work / "output/axis_fixture.mcpack").exists())
            request = {"schema":"aldeano-architecture/v1","name":"posada","template":"medieval_inn",
                       "theme":"medieval","seed":7,"features":["balcony","dormer"]}
            (work / "request.json").write_text(json.dumps(request),encoding="utf-8")
            run = subprocess.run([sys.executable,"-S","generator.py","request.json","--output","inn"],
                                 cwd=work,capture_output=True,text=True)
            self.assertEqual(run.returncode,0,run.stderr)
            self.assertTrue((work / "inn/posada.request.json").exists())

    def test_cli_errors_and_no_silent_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            out = str(Path(folder) / "output")
            command = [sys.executable, "-S", str(ROOT / "generator.py"),
                       str(ROOT / "tests/fixtures/axis.build.json"), "--output", out]
            first = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            second = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(second.returncode, 2)
            self.assertIn("Ya existen", json.loads(second.stderr)["error"])
            third = subprocess.run(command + ["--overwrite"], capture_output=True, text=True)
            self.assertEqual(third.returncode, 0, third.stderr)

    def test_catalog_files_match_runtime(self):
        for name, expected in g.JAVA_PROFILES.items():
            actual = json.loads((ROOT / f"catalog/profiles/{name}.json").read_text())
            for key, value in expected.items():
                self.assertEqual(actual[key], value)
        catalog = json.loads((ROOT / "catalog/canonical.json").read_text())
        self.assertEqual(set(catalog), set(g.MATERIALS))
        for m, (name, states, color) in g.MATERIALS.items():
            self.assertEqual(catalog[m]["bedrock"], "minecraft:" + name)
            self.assertEqual(catalog[m]["bedrock_states"], states)


if __name__ == "__main__":
    unittest.main()
