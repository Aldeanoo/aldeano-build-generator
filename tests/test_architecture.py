import copy
import io
import json
from pathlib import Path
import sys
import unittest
import xml.etree.ElementTree as ET

import jsonschema
import nbtlib

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import generator as g
import architect as a
from test_generator import fixture,parsed


def request():
    return json.loads((ROOT/"examples/posada.request.json").read_text(encoding="utf-8"))


class ArchitectureTests(unittest.TestCase):
    def test_request_schema(self):
        schema=json.loads((ROOT/"schema/aldeano-architecture-v1.schema.json").read_text())
        jsonschema.validate(request(),schema)

    def test_every_theme_and_optional_features(self):
        for theme in a.THEMES:
            for features in ([],sorted(a.FEATURES)):
                with self.subTest(theme=theme,features=features):
                    r=request();r["theme"]=theme;r["features"]=features
                    b=a.build_architecture(r)
                    g.validate_build(b)
                    outputs,report=g.generate(r)
                    self.assertTrue(report["validation"]["passed"])
                    self.assertEqual(json.loads(outputs[r["name"]+".request.json"]),r)
                    self.assertFalse(report["validation"]["minecraft_tested"])

    def test_deterministic_seed_and_request_not_mutated(self):
        r=request();before=copy.deepcopy(r)
        first=a.build_architecture(r);second=a.build_architecture(r)
        self.assertEqual(first,second)
        self.assertEqual(r,before)

    def test_removed_features_really_removed(self):
        r=request();r["features"]=[]
        b=a.build_architecture(r)
        self.assertNotIn("oak_leaves",b["palette"])
        self.assertNotIn("bricks",b["palette"])
        self.assertNotIn("red_carpet",b["palette"])

    def test_invalid_requests_fail(self):
        cases=[]
        for key,value in (("template","castle"),("theme","unknown"),("seed",True),
                          ("seed",-1),("features",["garden","garden"]),
                          ("features",["water"]),("name","../bad")):
            r=request();r[key]=value;cases.append(r)
        for r in cases:
            with self.subTest(r=r),self.assertRaises(ValueError):
                a.build_architecture(r)

    def test_builder_reports_bounds_instead_of_cropping(self):
        b=a.Builder("test",[10,10,10])
        with self.assertRaises(ValueError):
            b.fill([-1,0,0],[2,2,2],"stone")
        with self.assertRaises(ValueError):
            b.roof(0,9,0,9,9,"spruce")

    def test_real_door_halves_survive_decoration(self):
        volume=g.compile_volume(a.build_architecture(request()))
        sx,sy,sz=volume["size"]
        def material(x,y,z):
            idx=volume["cells"][(x*sy+y)*sz+z]
            return volume["palette"][idx] if idx>=0 else None
        self.assertEqual(material(16,5,8),"spruce_door_lower")
        self.assertEqual(material(16,6,8),"spruce_door_upper")
        self.assertEqual(material(16,13,7),"spruce_door_lower")
        self.assertEqual(material(16,14,7),"spruce_door_upper")


class DetailedStateTests(unittest.TestCase):
    def test_bedrock_byte_and_int_types(self):
        b=fixture()
        b["palette"]={"step":"spruce_stairs_north","door":"spruce_door_upper",
                      "lower":"spruce_door_lower"}
        b["ops"]=[{"op":"set","at":[0,0,0],"block":"step"},
                  {"op":"set","at":[1,1,0],"block":"door"},
                  {"op":"set","at":[1,0,0],"block":"lower"}]
        out,_=g.generate(b)
        root=parsed(out["axis_fixture.mcstructure"],little=True)
        palette=root["structure"]["palette"]["default"]["block_palette"]
        stairs=next(p for p in palette if p["name"]=="minecraft:spruce_stairs")
        self.assertIsInstance(stairs["states"]["upside_down_bit"],nbtlib.Byte)
        self.assertIsInstance(stairs["states"]["weirdo_direction"],nbtlib.Int)
        self.assertEqual(stairs["states"]["weirdo_direction"],3)

    def test_java_properties_and_real_ids_for_both_profiles(self):
        b=fixture();b["palette"]={"step":"spruce_stairs_north"}
        b["ops"]=[{"op":"set","at":[0,0,0],"block":"step"}]
        for profile in g.JAVA_PROFILES:
            out,_=g.generate(b,java_profile=profile)
            root=parsed(out["axis_fixture.nbt"],zipped=True)
            state=root["palette"][0]
            modern=profile=="java-26.3"
            self.assertEqual(state["id" if modern else "Name"],"minecraft:spruce_stairs")
            props=state["properties" if modern else "Properties"]
            self.assertEqual(props["facing"],"north")
            self.assertEqual(props["half"],"bottom")

    def test_detail_catalog_snapshot(self):
        self.assertEqual(g.DETAILS,json.loads((ROOT/"catalog/details.json").read_text()))

    def test_orphan_door_is_rejected_before_export(self):
        for material in ("spruce_door_lower","spruce_door_upper"):
            b=fixture();b["palette"]={"door":material}
            b["ops"]=[{"op":"set","at":[0,0,0],"block":"door"}]
            with self.assertRaisesRegex(g.BuildError,"Puerta"):
                g.generate(b)

    def test_paired_door_is_checked_in_report(self):
        _,report=g.generate(request())
        self.assertEqual(report["door_pairs"],2)
        self.assertIn("paired_door_halves",report["validation"]["checks"])

    def test_preview_uses_partial_shapes(self):
        slab=g.preview_boxes("spruce_slab_bottom")[0]
        self.assertEqual(slab[4]-.5,0)
        stairs=g.preview_boxes("spruce_stairs_north")
        self.assertEqual(len(stairs),2)
        self.assertEqual(stairs[1],(0,.5,0,1,1,.5))
        root=ET.fromstring(g.preview_svg(g.compile_volume(fixture())))
        self.assertTrue(any(n.tag.endswith("polygon") for n in root))

    def test_review_is_diagnostics_not_aesthetic_grade(self):
        b=fixture();b["palette"]={"s":"stone"}
        b["ops"]=[{"op":"set","at":[0,0,0],"block":"s"}]
        review=g.analyze_quality(g.compile_volume(b))
        self.assertNotIn("score",review)
        self.assertTrue(review["warnings"])
        self.assertTrue(review["visual_review_required"])
