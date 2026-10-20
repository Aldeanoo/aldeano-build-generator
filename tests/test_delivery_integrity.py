"""Delivery and corruption regressions; independent NBT reader for mutations."""
import copy
import gzip
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import nbtlib

from test_generator import fixture, parsed, ROOT
import generator as g


def repack(root, little=False):
    stream = io.BytesIO()
    root.write(stream, byteorder="little" if little else "big")
    return stream.getvalue() if little else gzip.compress(stream.getvalue(), mtime=0)


class DeliveryTests(unittest.TestCase):
    def test_minimal_deliveries_have_exactly_requested_files(self):
        for delivery, expected in (
            ("mcstructure", {"axis_fixture.mcstructure"}),
            ("nbt", {"axis_fixture.nbt"}),
            ("structures", {"axis_fixture.nbt", "axis_fixture.mcstructure"}),
        ):
            outputs, report = g.generate(fixture(), delivery=delivery)
            self.assertEqual(set(outputs), expected)
            self.assertEqual(set(report["sha256"]), expected)
            self.assertTrue(report["validation"]["passed"])
            for name, blob in outputs.items():
                self.assertTrue(g.verify_structure(blob, name.rsplit(".", 1)[1])["passed"])

    def test_conflicting_edition_and_delivery_rejected(self):
        for edition, delivery in (("java", "mcstructure"), ("both", "nbt"), ("java", "structures")):
            with self.assertRaises(g.BuildError):
                g.generate(fixture(), edition=edition, delivery=delivery)

    def test_java_cli_requires_profile_and_minimal_roundtrip(self):
        with tempfile.TemporaryDirectory() as folder:
            base = [sys.executable, "-S", str(ROOT / "generator.py")]
            command = base + [str(ROOT / "tests/fixtures/axis.build.json"),
                              "--delivery", "nbt", "--output", folder]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn("--java-profile", result.stderr)
            result = subprocess.run(command + ["--java-profile", "java-1.21.1"],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            self.assertTrue(report["validation"]["disk_readback"])
            self.assertEqual({p.name for p in Path(folder).iterdir()}, {"axis_fixture.nbt"})
            path = Path(folder) / "axis_fixture.nbt"
            check = subprocess.run(base + ["--verify", str(path), "--java-profile", "java-1.21.1"],
                                   capture_output=True, text=True)
            self.assertEqual(check.returncode, 0, check.stderr)
            self.assertEqual(json.loads(check.stdout)["verification"]["sha256"],
                             report["sha256"][path.name])
            self.assertIn("Name", nbtlib.load(path)["palette"][0])
            path.write_bytes(path.read_bytes()[:-3])
            check = subprocess.run(base + ["--verify", str(path)], capture_output=True, text=True)
            self.assertEqual(check.returncode, 2)
            self.assertFalse(json.loads(check.stderr)["ok"])

    def test_bedrock_minimal_cli_does_not_require_java_profile(self):
        with tempfile.TemporaryDirectory() as folder:
            result = subprocess.run([sys.executable, "-S", str(ROOT / "generator.py"),
                                     str(ROOT / "tests/fixtures/axis.build.json"), "--delivery",
                                     "mcstructure", "--output", folder], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual({p.name for p in Path(folder).iterdir()}, {"axis_fixture.mcstructure"})

    def test_disk_write_roundtrip_and_no_silent_overwrite(self):
        outputs, _ = g.generate(fixture(), delivery="structures")
        with tempfile.TemporaryDirectory() as folder:
            g.write_outputs(outputs, folder)
            self.assertEqual({p.name: p.read_bytes() for p in Path(folder).iterdir()}, outputs)
            with self.assertRaisesRegex(g.BuildError, "Ya existen"):
                g.write_outputs(outputs, folder)
            g.write_outputs(outputs, folder, overwrite=True)

    def test_bad_binary_not_published_and_staging_cleaned(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(g.BuildError):
                g.write_outputs({"broken.nbt": b"not an NBT file"}, folder)
            self.assertEqual(list(Path(folder).iterdir()), [])

    def test_final_readback_detects_disk_corruption(self):
        outputs, _ = g.generate(fixture(), delivery="nbt")
        replace = g.os.replace

        def damage(source, target):
            replace(source, target)
            target.write_bytes(target.read_bytes()[:-1])

        with tempfile.TemporaryDirectory() as folder, mock.patch.object(g.os, "replace", side_effect=damage):
            with self.assertRaisesRegex(g.BuildError, "lectura final"):
                g.write_outputs(outputs, folder)


class CorruptionTests(unittest.TestCase):
    def setUp(self):
        self.volume = g.compile_volume(fixture())

    def test_java_gzip_crc_truncation_trailing_data_and_fake_files(self):
        blob = g.export_java_structure(self.volume)
        damaged = bytearray(blob)
        damaged[-8] ^= 1  # CRC32 trailer, not just a damaged header.
        for value in (blob[:8], blob[:-1], bytes(damaged), blob + b"garbage", blob + blob,
                      b"", b'{"palette":[]}', gzip.decompress(blob),
                      gzip.compress(g.export_mcstructure(self.volume))):
            with self.subTest(length=len(value)), self.assertRaises(g.BuildError):
                g.verify_structure(value, "nbt")

    def test_java_profile_mismatch_rejected_for_both_directions(self):
        for profile, other in (("java-1.21.1", "java-26.3"), ("java-26.3", "java-1.21.1")):
            blob = g.export_java_structure(self.volume, profile)
            self.assertTrue(g.verify_structure(blob, "nbt", profile)["passed"])
            with self.assertRaisesRegex(g.BuildError, "DataVersion"):
                g.verify_structure(blob, "nbt", other)

    def test_java_invalid_coordinates_palette_indices_and_tag_types(self):
        original = parsed(g.export_java_structure(self.volume), zipped=True)
        mutations = []
        root = copy.deepcopy(original); root["blocks"][0]["state"] = nbtlib.Int(-1); mutations.append(root)
        root = copy.deepcopy(original); root["blocks"][0]["state"] = nbtlib.Int(999); mutations.append(root)
        root = copy.deepcopy(original); root["blocks"][0]["pos"][0] = nbtlib.Int(48); mutations.append(root)
        root = copy.deepcopy(original); root["blocks"].append(copy.deepcopy(root["blocks"][0])); mutations.append(root)
        root = copy.deepcopy(original); root["blocks"][0]["state"] = nbtlib.Byte(0); mutations.append(root)
        root = copy.deepcopy(original); root["palette"][0]["id"] = root["palette"][0].pop("Name"); mutations.append(root)
        root = copy.deepcopy(original); root["palette"][0]["Name"] = nbtlib.String("minecraft:not_real"); mutations.append(root)
        for root in mutations:
            with self.subTest(root=root.keys()), self.assertRaises(g.BuildError):
                g.verify_structure(repack(root), "nbt")

    def test_bedrock_invalid_layers_indices_types_and_endianness(self):
        original = parsed(g.export_mcstructure(self.volume), little=True)
        mutations = []
        root = copy.deepcopy(original); root["structure"]["block_indices"][0][0] = nbtlib.Int(999); mutations.append(root)
        root = copy.deepcopy(original); root["structure"]["block_indices"][1].pop(); mutations.append(root)
        root = copy.deepcopy(original); root["structure"]["block_indices"][1][0] = nbtlib.Int(0); mutations.append(root)
        root = copy.deepcopy(original); root["format_version"] = nbtlib.Byte(1); mutations.append(root)
        for root in mutations:
            with self.assertRaises(g.BuildError):
                g.verify_structure(repack(root, little=True), "mcstructure")
        stream = io.BytesIO(); original.write(stream, byteorder="big")
        for value in (stream.getvalue(), g.export_mcstructure(self.volume)[:-1]):
            with self.assertRaises(g.BuildError):
                g.verify_structure(value, "mcstructure")

    def test_bedrock_boolean_state_must_be_byte(self):
        build = fixture()
        build["palette"] = {"step": "spruce_stairs_north"}
        build["ops"] = [{"op": "set", "at": [0, 0, 0], "block": "step"}]
        blob = g.export_mcstructure(g.compile_volume(build))
        root = parsed(blob, little=True)
        entry = root["structure"]["palette"]["default"]["block_palette"][0]
        entry["states"]["upside_down_bit"] = nbtlib.Int(0)
        with self.assertRaisesRegex(g.BuildError, "Tipo NBT"):
            g.verify_structure(repack(root, little=True), "mcstructure")


if __name__ == "__main__":
    unittest.main()
