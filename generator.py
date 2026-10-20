#!/usr/bin/env python3
"""Aldeano Build Generator. Python 3.10+, standard library only. MIT."""
import argparse
from collections import Counter
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import re
import struct
import sys
import tempfile
import uuid
import zipfile
import zlib

VERSION = "0.2.1"
DEFAULT_JAVA_PROFILE = "java-1.21.1"
DELIVERIES = ("full", "mcstructure", "nbt", "structures")
MAX_NBT_BYTES = 8 * 1024 * 1024
SCHEMA = "aldeano-build/v1"
MAX_BYTES = 262144
MAX_OPS = 512
MAX_WRITES = 4000000
BEDROCK_VERSION = 18168865
BEDROCK_ENGINE = [1, 26, 30]
REPO = "https://github.com/Aldeanoo/aldeano-build-generator"
JAVA_PROFILES = {
    "java-26.3": {"data_version": 5023, "format": 121, "modern": True},
    "java-1.21.1": {"data_version": 3955, "format": 48, "modern": False},
}
# Canonical name: (Bedrock name, states, preview color). Java uses canonical IDs.
MATERIALS = {
    "air": ("air", {}, "#ffffff"),
    "stone": ("stone", {}, "#858585"),
    "cobblestone": ("cobblestone", {}, "#737373"),
    "stone_bricks": ("stone_bricks", {}, "#96918a"),
    "mossy_stone_bricks": ("mossy_stone_bricks", {}, "#71826b"),
    "cracked_stone_bricks": ("cracked_stone_bricks", {}, "#7f7c76"),
    "bricks": ("brick_block", {}, "#a76552"),
    "oak_planks": ("oak_planks", {}, "#b8945f"),
    "spruce_planks": ("spruce_planks", {}, "#765637"),
    "birch_planks": ("birch_planks", {}, "#d7c88e"),
    "dark_oak_planks": ("dark_oak_planks", {}, "#49301f"),
    "acacia_planks": ("acacia_planks", {}, "#b9653c"),
    "jungle_planks": ("jungle_planks", {}, "#b7825b"),
    "mangrove_planks": ("mangrove_planks", {}, "#793c36"),
    "cherry_planks": ("cherry_planks", {}, "#dcafa8"),
    "bamboo_planks": ("bamboo_planks", {}, "#c9b556"),
    "glass": ("glass", {}, "#a4d5df"),
    "white_wool": ("white_wool", {}, "#e7e5dd"),
    "gray_wool": ("gray_wool", {}, "#44474b"),
    "black_wool": ("black_wool", {}, "#242426"),
    "red_wool": ("red_wool", {}, "#a52d28"),
    "white_concrete": ("white_concrete", {}, "#dadcdd"),
    "gray_concrete": ("gray_concrete", {}, "#373a3e"),
    "black_concrete": ("black_concrete", {}, "#181a20"),
    "red_concrete": ("red_concrete", {}, "#8e2525"),
    "terracotta": ("hardened_clay", {}, "#9e6247"),
    "white_terracotta": ("white_terracotta", {}, "#d0ad9e"),
    "brown_terracotta": ("brown_terracotta", {}, "#583e31"),
    "sandstone": ("sandstone", {}, "#d6c694"),
    "smooth_sandstone": ("smooth_sandstone", {}, "#dfd0a4"),
    "red_sandstone": ("red_sandstone", {}, "#b76527"),
    "quartz_block": ("quartz_block", {"pillar_axis": "y"}, "#e8e3da"),
    "smooth_quartz": ("smooth_quartz", {"pillar_axis": "y"}, "#eeebe5"),
    "gold_block": ("gold_block", {}, "#e9ca44"),
    "iron_block": ("iron_block", {}, "#cfd0cd"),
    "glowstone": ("glowstone", {}, "#c6a568"),
    "sea_lantern": ("sea_lantern", {}, "#b5d4c6"),
}
# BEGIN DETAIL CATALOG
DETAILS = {}


def _detail(alias, name, props, states, color, shape="cube", bedrock=None):
    DETAILS[alias] = {"java": name, "properties": props, "bedrock": bedrock or name,
                     "states": states, "color": color, "shape": shape}


for wood, color in (("oak", "#96734b"), ("dark_oak", "#514031")):
    for axis in "xyz":
        _detail(wood+"_log_"+axis, wood+"_log", {"axis": axis}, {"pillar_axis": axis}, color)
for family, color in (("deepslate_tile", "#3d4c58"), ("spruce", "#765637"), ("stone_brick", "#96918a")):
    for facing, direction in (("north", 3), ("south", 2), ("east", 0), ("west", 1)):
        _detail(family+"_stairs_"+facing, family+"_stairs",
                {"facing": facing, "half": "bottom", "shape": "straight", "waterlogged": "false"},
                {"upside_down_bit": False, "weirdo_direction": direction}, color, "stairs")
for family, color in (("spruce", "#765637"), ("oak", "#b8945f"),
                      ("stone_brick", "#96918a"), ("deepslate_tile", "#3d4c58")):
    for half in ("bottom", "top"):
        _detail(family+"_slab_"+half, family+"_slab",
                {"type": half, "waterlogged": "false"},
                {"minecraft:vertical_half": half}, color, "slab")
for facing, direction in (("north", 3), ("south", 2), ("east", 0), ("west", 1)):
    _detail("spruce_shutter_"+facing, "spruce_trapdoor",
            {"facing": facing, "half": "bottom", "open": "true", "powered": "false", "waterlogged": "false"},
            {"direction": direction, "open_bit": True, "upside_down_bit": False}, "#816240", "shutter")
for half in ("lower", "upper"):
    _detail("spruce_door_"+half, "spruce_door",
            {"facing": "north", "half": half, "hinge": "left", "open": "false", "powered": "false"},
            {"door_hinge_bit": False, "minecraft:cardinal_direction": "east", "open_bit": False,
             "upper_block_bit": half == "upper"}, "#785a39", "door")
for hanging in (True, False):
    _detail("lantern_hanging" if hanging else "lantern", "lantern",
            {"hanging": str(hanging).lower(), "waterlogged": "false"},
            {"hanging": hanging}, "#edb65a", "lantern")
_detail("oak_leaves", "oak_leaves",
        {"distance": "7", "persistent": "true", "waterlogged": "false"},
        {"persistent_bit": True, "update_bit": False}, "#6f8c48")
_detail("spruce_post", "spruce_fence",
        {"east": "false", "north": "false", "south": "false", "waterlogged": "false", "west": "false"},
        {}, "#765637", "post")
_detail("grass_block", "grass_block", {"snowy": "false"}, {}, "#8f9f62")
for name, color, shape in (("moss_block", "#778a4e", "cube"), ("moss_carpet", "#778a4e", "carpet"),
                           ("coarse_dirt", "#81634c", "cube"), ("dirt_path", "#a28d65", "path"),
                           ("flowering_azalea", "#7c9155", "bush"), ("poppy", "#c35b4e", "flower"),
                           ("dandelion", "#e3bf58", "flower"), ("red_carpet", "#993f3e", "carpet")):
    _detail(name, name, {}, {}, color, shape, "grass_path" if name == "dirt_path" else None)
MATERIALS.update({key: (d["bedrock"], d["states"], d["color"]) for key, d in DETAILS.items()})
# END DETAIL CATALOG
NAME = re.compile(r"[a-z][a-z0-9_]{0,47}\Z")


class BuildError(ValueError):
    """An actionable input or generated-output error."""


def _fail(message):
    raise BuildError(message)


def _keys(obj, required, where):
    if type(obj) is not dict or set(obj) != set(required):
        _fail(f"{where}: campos requeridos exactos: {', '.join(required)}")


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            _fail(f"Clave JSON repetida: {key}")
        result[key] = value
    return result


def parse_build(text):
    if not isinstance(text, str) or len(text.encode("utf-8")) > MAX_BYTES:
        _fail("El JSON supera 256 KiB o no es texto.")
    text = text.lstrip("\ufeff").strip()
    # Accept only one complete Markdown wrapper, not arbitrary prose.
    match = re.fullmatch(r"(?:```(?:json)?|~~~(?:json)?)\s*\n(.*?)\n(?:```|~~~)", text, re.S)
    if match:
        opening = text[:3]
        if text[-3:] != opening:
            _fail("El bloque Markdown no cierra con el mismo delimitador.")
        text = match.group(1)
    try:
        data = json.loads(text, object_pairs_hook=_pairs,
                          parse_constant=lambda value: _fail(f"Numero no valido: {value}"))
        pending = [(data, 0)]
        while pending:
            item, depth = pending.pop()
            if depth > 12:
                _fail("JSON demasiado anidado (maximo 12 niveles).")
            children = item.values() if type(item) is dict else item if type(item) is list else ()
            pending.extend((child, depth + 1) for child in children)
        return data
    except (json.JSONDecodeError, RecursionError) as error:
        _fail(f"JSON no valido o demasiado anidado: {error}")


def validate_build(data, max_size=32):
    if max_size not in (32, 48):
        _fail("El limite permitido es 32 o 48.")
    _keys(data, ("schema", "name", "size", "palette", "ops"), "Diseno")
    if data["schema"] != SCHEMA:
        _fail(f"schema debe ser {SCHEMA}.")
    if type(data["name"]) is not str or not NAME.fullmatch(data["name"]):
        _fail("name: usa una letra inicial y hasta 48 letras minusculas, numeros o _.")
    size = data["size"]
    if type(size) is not list or len(size) != 3 or any(
            type(n) is not int or not 1 <= n <= max_size for n in size):
        _fail(f"size: tres enteros entre 1 y {max_size}; orden [x, y, z].")
    palette = data["palette"]
    if type(palette) is not dict or not 1 <= len(palette) <= 64:
        _fail("palette: entre 1 y 64 alias.")
    for alias, material in palette.items():
        if not NAME.fullmatch(alias) or alias in ("constructor", "prototype"):
            _fail(f"Alias no valido: {alias}")
        if type(material) is not str or material not in MATERIALS:
            _fail(f"Material no permitido para {alias}: {material}")
    ops = data["ops"]
    if type(ops) is not list or not 1 <= len(ops) <= MAX_OPS:
        _fail(f"ops: entre 1 y {MAX_OPS} operaciones.")
    writes = 0
    for number, op in enumerate(ops, 1):
        where = f"Operacion {number}"
        if type(op) is not dict or op.get("op") not in ("set", "fill"):
            _fail(f"{where}: solo se admiten set y fill.")
        kind = op["op"]
        _keys(op, ("op", "at", "block") if kind == "set"
              else ("op", "from", "to", "block"), where)
        if type(op["block"]) is not str or op["block"] not in palette:
            _fail(f"{where}: alias block desconocido.")
        points = [op["at"]] if kind == "set" else [op["from"], op["to"]]
        for point in points:
            if type(point) is not list or len(point) != 3 or any(
                    type(n) is not int or not 0 <= n < size[i]
                    for i, n in enumerate(point)):
                _fail(f"{where}: coordenadas enteras dentro de size; recibido {point}.")
        volume = 1
        if kind == "fill":
            for low, high in zip(*points):
                if low > high:
                    _fail(f"{where}: from debe ser menor o igual que to en cada eje.")
                volume *= high - low + 1
        writes += volume
        if writes > MAX_WRITES:
            _fail(f"{where}: se supera el presupuesto de {MAX_WRITES} escrituras.")
    return data


def compile_volume(build):
    """Use Bedrock's z-fastest ordering; -1 means leave the world untouched."""
    sx, sy, sz = build["size"]
    materials = sorted({build["palette"][op["block"]] for op in build["ops"]})
    lookup = {material: i for i, material in enumerate(materials)}
    cells = [-1] * (sx * sy * sz)
    for op in build["ops"]:
        low = op["at"] if op["op"] == "set" else op["from"]
        high = low if op["op"] == "set" else op["to"]
        state = lookup[build["palette"][op["block"]]]
        row = [state] * (high[2] - low[2] + 1)
        for x in range(low[0], high[0] + 1):
            for y in range(low[1], high[1] + 1):
                start = (x * sy + y) * sz + low[2]
                cells[start:start + len(row)] = row
    return {"size": list(build["size"]), "palette": materials, "cells": cells}


def positions(volume):
    _, sy, sz = volume["size"]
    for i, state in enumerate(volume["cells"]):
        if state >= 0:
            yield [i // (sy * sz), (i // sz) % sy, i % sz], state


# NBT tags are tuples (tag ID, payload); list payload is (child tag ID, values).
def I(value): return (3, value)
def S(value): return (8, value)
def C(value): return (10, value)
def L(child, values): return (9, (child, values))


def java_state(material, modern=True):
    detail = DETAILS.get(material, {})
    result = {"id" if modern else "Name": "minecraft:" + detail.get("java", material)}
    if detail.get("properties"):
        result["properties" if modern else "Properties"] = detail["properties"]
    return result


def _bedrock_state(value):
    if type(value) is bool:
        return (1, int(value))
    return I(value) if type(value) is int else S(value)


def write_nbt(root, little=False):
    endian = "<" if little else ">"

    def string(value):
        # NBT output uses ASCII identifiers only (also valid modified UTF-8).
        encoded = value.encode("ascii")
        return struct.pack(endian + "H", len(encoded)) + encoded

    def payload(kind, value):
        if kind == 1:
            return struct.pack("b", value)
        if kind == 3:
            return struct.pack(endian + "i", value)
        if kind == 8:
            return string(value)
        if kind == 9:
            child, values = value
            header = bytes([child]) + struct.pack(endian + "i", len(values))
            if child == 3:
                return header + struct.pack(endian + f"{len(values)}i", *values)
            return header + b"".join(payload(child, item) for item in values)
        if kind == 10:
            return b"".join(bytes([tag[0]]) + string(name) + payload(*tag)
                            for name, tag in value.items()) + b"\x00"
        _fail(f"Tipo NBT no soportado: {kind}")
    return b"\x0a\x00\x00" + payload(10, root)


def read_nbt(blob, little=False, tag_types=None):
    """Bounded structural check for the subset we emit, not a general importer."""
    stream = io.BytesIO(blob)
    endian = "<" if little else ">"

    def take(n):
        if n < 0 or n > len(blob):
            _fail("Longitud NBT no valida.")
        data = stream.read(n)
        if len(data) != n:
            _fail("NBT truncado.")
        return data

    def number(fmt):
        return struct.unpack(endian + fmt, take(struct.calcsize(fmt)))[0]

    def string():
        return take(number("H")).decode("ascii")

    def payload(kind, depth=0, path=()):
        if depth > 32:
            _fail("NBT demasiado anidado.")
        if tag_types is not None and kind != 9:
            tag_types.setdefault(path, set()).add((kind, None))
        if kind == 1:
            return number("b")
        if kind == 3:
            return number("i")
        if kind == 8:
            return string()
        if kind == 9:
            child = number("B")
            count = number("i")
            if tag_types is not None:
                tag_types.setdefault(path, set()).add((9, child))
            if not 0 <= count <= 48 ** 3:
                _fail("Lista NBT fuera de limite.")
            if child not in (1, 3, 8, 9, 10):
                _fail("Tipo de lista NBT inesperado.")
            return [payload(child, depth + 1, path + ("*",)) for _ in range(count)]
        if kind == 10:
            result = {}
            while True:
                child = number("B")
                if child == 0:
                    return result
                key = string()
                if key in result:
                    _fail("Clave NBT repetida.")
                result[key] = payload(child, depth + 1, path + (key,))
        _fail(f"Tipo NBT inesperado: {kind}")

    if take(3) != b"\x0a\x00\x00":
        _fail("Raiz NBT inesperada.")
    result = payload(10)
    if stream.read(1):
        _fail("Bytes sobrantes al final del NBT.")
    return result


def read_structure(blob, file_type, java_profile=None):
    """Strict validator for our own exports, including tag types and GZIP CRC."""
    if not blob or len(blob) > MAX_NBT_BYTES:
        _fail("Estructura vacia o demasiado grande.")
    if file_type not in ("nbt", "mcstructure"):
        _fail("Solo se verifican .nbt y .mcstructure del generador.")
    types = {}
    if file_type == "nbt":
        if not blob.startswith(b"\x1f\x8b"):
            _fail("Java requiere un NBT binario GZIP; no texto, ZIP ni Bedrock.")
        try:
            decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
            raw = decoder.decompress(blob, MAX_NBT_BYTES + 1)
            if (len(raw) > MAX_NBT_BYTES or not decoder.eof
                    or decoder.unused_data or decoder.unconsumed_tail):
                _fail("GZIP truncado, con bytes sobrantes o fuera de limite.")
        except zlib.error as error:
            _fail(f"GZIP corrupto (cabecera, datos o CRC): {error}")
    else:
        raw = blob
    try:
        root = read_nbt(raw, little=file_type == "mcstructure", tag_types=types)
    except UnicodeError:
        _fail("Identificador NBT no valido para este generador.")

    def tag(path, kind, child=None):
        if types.get(tuple(path.split("/")) if path else ()) != {(kind, child)}:
            _fail(f"Tipo NBT incorrecto en {path or 'raiz'}.")

    def vector(value):
        return (type(value) is list and len(value) == 3
                and all(type(n) is int for n in value))

    tag("", 10)
    tag("size", 9, 3)
    size = root.get("size")
    if not vector(size) or any(not 1 <= n <= 48 for n in size):
        _fail("Dimensiones de estructura no validas.")
    if file_type == "nbt":
        _keys(root, ("DataVersion", "size", "palette", "blocks", "entities"), "NBT Java")
        tag("DataVersion", 3)
        detected = next((p for p, c in JAVA_PROFILES.items()
                         if c["data_version"] == root["DataVersion"]), None)
        if detected is None or (java_profile is not None and java_profile != detected):
            _fail("El DataVersion del NBT no corresponde al perfil Java solicitado.")
        modern = JAVA_PROFILES[detected]["modern"]
        tag("palette", 9, 10)
        tag("blocks", 9, 10)
        tag("entities", 9, 10)
        palette = root["palette"]
        if not 1 <= len(palette) <= 64:
            _fail("Paleta Java fuera de limite.")
        allowed = [java_state(m, modern) for m in MATERIALS]
        key, props = ("id", "properties") if modern else ("Name", "Properties")
        tag("palette/*/" + key, 8)
        for entry in palette:
            if entry not in allowed:
                _fail("Identificador, propiedades o formato de paleta Java incorrectos.")
        if any(props in entry for entry in palette):
            tag("palette/*/" + props, 10)
            for entry in palette:
                for prop in entry.get(props, {}):
                    tag("palette/*/" + props + "/" + prop, 8)
        if not root["blocks"] or root["entities"]:
            _fail("Se requieren bloques y entities vacio.")
        tag("blocks/*/pos", 9, 3)
        tag("blocks/*/state", 3)
        seen = set()
        for block in root["blocks"]:
            _keys(block, ("pos", "state"), "Bloque Java")
            pos, state = block["pos"], block["state"]
            if (not vector(pos) or any(not 0 <= n < size[i] for i, n in enumerate(pos))
                    or type(state) is not int or not 0 <= state < len(palette)
                    or tuple(pos) in seen):
                _fail("Coordenada o indice de paleta Java no valido o repetido.")
            seen.add(tuple(pos))
    else:
        _keys(root, ("format_version", "size", "structure_world_origin", "structure"), "NBT Bedrock")
        tag("format_version", 3)
        tag("structure_world_origin", 9, 3)
        if root["format_version"] != 1 or root["structure_world_origin"] != [0, 0, 0]:
            _fail("Version u origen Bedrock no validos.")
        structure = root["structure"]
        _keys(structure, ("block_indices", "entities", "palette"), "Estructura Bedrock")
        tag("structure", 10)
        tag("structure/block_indices", 9, 9)
        tag("structure/block_indices/*", 9, 3)
        tag("structure/entities", 9, 10)
        tag("structure/palette", 10)
        _keys(structure["palette"], ("default",), "Paleta Bedrock")
        default = structure["palette"]["default"]
        _keys(default, ("block_palette", "block_position_data"), "Paleta por defecto")
        prefix = "structure/palette/default/"
        tag(prefix.rstrip("/"), 10)
        tag(prefix + "block_palette", 9, 10)
        tag(prefix + "block_position_data", 10)
        palette = default["block_palette"]
        if not 1 <= len(palette) <= 64 or default["block_position_data"] or structure["entities"]:
            _fail("Paleta, datos de bloque o entidades Bedrock inesperados.")
        tag(prefix + "block_palette/*/name", 8)
        tag(prefix + "block_palette/*/version", 3)
        tag(prefix + "block_palette/*/states", 10)
        for entry in palette:
            matches = [s for n, s, _ in MATERIALS.values()
                       if entry == {"name": "minecraft:" + n, "states": s, "version": BEDROCK_VERSION}]
            if not matches:
                _fail("Identificador o estados Bedrock no validos.")
            source = matches[0]
            for key in entry["states"]:
                kind = 1 if type(source[key]) is bool else 3 if type(source[key]) is int else 8
                tag(prefix + "block_palette/*/states/" + key, kind)
        layers = structure["block_indices"]
        count = size[0] * size[1] * size[2]
        if (len(layers) != 2 or any(len(row) != count for row in layers)
                or any(not -1 <= index < len(palette) for index in layers[0])
                or any(index != -1 for index in layers[1])):
            _fail("Capas o indices Bedrock incorrectos.")
    return root


def verify_structure(blob, file_type, java_profile=None):
    root = read_structure(blob, file_type, java_profile)
    return {"passed": True, "format": file_type, "bytes": len(blob), "size": root["size"],
            "data_version": root.get("DataVersion"),
            "sha256": hashlib.sha256(blob).hexdigest(), "minecraft_tested": False}


def export_mcstructure(volume):
    palette = []
    for material in volume["palette"]:
        name, states, _ = MATERIALS[material]
        palette.append({
            "name": S("minecraft:" + name),
            "states": C({key: _bedrock_state(value) for key, value in states.items()}),
            "version": I(BEDROCK_VERSION),
        })
    return write_nbt({
        "format_version": I(1), "size": L(3, volume["size"]),
        "structure_world_origin": L(3, [0, 0, 0]),
        "structure": C({
            "block_indices": L(9, [(3, volume["cells"]), (3, [-1] * len(volume["cells"]))]),
            "entities": L(10, []),
            "palette": C({"default": C({
                "block_palette": L(10, palette), "block_position_data": C({})
            })}),
        }),
    }, little=True)


def export_java_structure(volume, profile=DEFAULT_JAVA_PROFILE):
    config = JAVA_PROFILES[profile]
    palette = []
    for material in volume["palette"]:
        state = java_state(material, config["modern"])
        palette.append({key: C({k: S(v) for k, v in value.items()})
                        if type(value) is dict else S(value) for key, value in state.items()})
    root = {
        "DataVersion": I(config["data_version"]), "size": L(3, volume["size"]),
        "palette": L(10, palette),
        "blocks": L(10, [{"pos": L(3, pos), "state": I(state)}
                         for pos, state in positions(volume)]),
        "entities": L(10, []),
    }
    return gzip.compress(write_nbt(root), mtime=0)


def _json(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def _zip(files):
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, contents in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(2024, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, contents)
    return stream.getvalue()


def package_bedrock(structure, name, pack_version=(1, 0, 0)):
    identity = REPO + "/build/" + name
    manifest = {
        "format_version": 2,
        "header": {
            "name": "Aldeano: " + name,
            "description": "Estructura generada con Aldeano Build Generator",
            "uuid": str(uuid.uuid5(uuid.NAMESPACE_URL, identity + "/header")),
            "version": list(pack_version), "min_engine_version": BEDROCK_ENGINE,
        },
        "modules": [{
            "type": "data",
            "uuid": str(uuid.uuid5(uuid.NAMESPACE_URL, identity + "/data")),
            "version": list(pack_version),
        }],
    }
    return _zip({"manifest.json": _json(manifest),
                 f"structures/aldeano/{name}.mcstructure": structure})


def package_java(structure, name, profile=DEFAULT_JAVA_PROFILE):
    config = JAVA_PROFILES[profile]
    pack = {"description": "Aldeano: " + name}
    if config["modern"]:
        pack.update(min_format=[config["format"], 0], max_format=[config["format"], 0])
    else:
        pack["pack_format"] = config["format"]
    return _zip({"pack.mcmeta": _json({"pack": pack}),
                 f"data/aldeano/structure/{name}.nbt": structure})


def validate_outputs(outputs, volume, name, edition, java_profile):
    checks = []
    if edition in ("bedrock", "both"):
        blob = outputs[name + ".mcstructure"]
        root = read_structure(blob, "mcstructure")
        structure = root["structure"]
        expected_palette = [{"name": "minecraft:" + MATERIALS[m][0],
                             "states": MATERIALS[m][1], "version": BEDROCK_VERSION}
                            for m in volume["palette"]]
        if (root["format_version"] != 1 or root["size"] != volume["size"]
                or root["structure_world_origin"] != [0, 0, 0]
                or structure["block_indices"] != [volume["cells"], [-1] * len(volume["cells"])]
                or structure["palette"]["default"]["block_palette"] != expected_palette
                or structure["entities"] != []):
            _fail("La validacion semantica de Bedrock ha fallado.")
        with zipfile.ZipFile(io.BytesIO(outputs[name + ".mcpack"])) as pack:
            path = f"structures/aldeano/{name}.mcstructure"
            manifest = json.loads(pack.read("manifest.json"))
            if set(pack.namelist()) != {"manifest.json", path} or pack.read(path) != blob:
                _fail("Contenido inesperado en el mcpack.")
            if (manifest["modules"][0]["type"] != "data"
                    or manifest["header"]["uuid"] == manifest["modules"][0]["uuid"]):
                _fail("Manifiesto Bedrock no valido.")
        checks += ["bedrock_nbt_little_endian", "bedrock_geometry_and_palette", "mcpack_contents"]
    if edition in ("java", "both"):
        blob = outputs[name + ".nbt"]
        root = read_structure(blob, "nbt", java_profile)
        config = JAVA_PROFILES[java_profile]
        expected_palette = [java_state(m, config["modern"]) for m in volume["palette"]]
        expected_blocks = [{"pos": pos, "state": state} for pos, state in positions(volume)]
        if (root["DataVersion"] != config["data_version"] or root["size"] != volume["size"]
                or root["palette"] != expected_palette or root["blocks"] != expected_blocks
                or root["entities"] != []):
            _fail("La validacion semantica de Java ha fallado.")
        with zipfile.ZipFile(io.BytesIO(outputs[name + ".datapack.zip"])) as pack:
            path = f"data/aldeano/structure/{name}.nbt"
            if set(pack.namelist()) != {"pack.mcmeta", path} or pack.read(path) != blob:
                _fail("Contenido inesperado en el datapack.")
            if json.loads(pack.read("pack.mcmeta"))["pack"].get(
                    "min_format" if config["modern"] else "pack_format") != (
                    [config["format"], 0] if config["modern"] else config["format"]):
                _fail("Metadatos de datapack no validos.")
        checks += ["java_gzip_nbt_big_endian", "java_geometry_and_palette", "datapack_contents"]
    return checks


def preview_ortho_svg(volume):
    """Orthographic projections, using the same final cells as both exporters."""
    sx, sy, sz = volume["size"]
    cells, palette = volume["cells"], volume["palette"]
    scale, gap = 12, 34
    width = (sx + sz) * scale + gap * 3
    height = (sy + sz) * scale + gap * 3
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
           '<rect width="100%" height="100%" fill="#f4f1e9"/>',
           '<g font-family="sans-serif" font-size="12" fill="#243029">',
           f'<text x="{gap}" y="20">Planta (X/Z)</text>',
           f'<text x="{gap}" y="{sz * scale + gap + 20}">Frente (X/Y)</text>',
           f'<text x="{sx * scale + gap * 2}" y="{sz * scale + gap + 20}">Lateral (Z/Y)</text></g>']
    def visible(x, y, z):
        idx = cells[(x * sy + y) * sz + z]
        return palette[idx] if idx >= 0 and palette[idx] != "air" else None
    def square(x, y, material):
        if material:
            color = MATERIALS[material][2]
            svg.append(f'<rect x="{x}" y="{y}" width="{scale}" height="{scale}" fill="{color}" stroke="#000" stroke-opacity=".12"/>')
    for x in range(sx):
        for z in range(sz):
            material = next((m for y in range(sy - 1, -1, -1)
                             if (m := visible(x, y, z))), None)
            square(gap + x * scale, gap + z * scale, material)
    base = sz * scale + gap * 2
    for y in range(sy):
        for x in range(sx):
            material = next((m for z in range(sz) if (m := visible(x, y, z))), None)
            square(gap + x * scale, base + (sy - 1 - y) * scale, material)
        for z in range(sz):
            material = next((m for x in range(sx - 1, -1, -1)
                             if (m := visible(x, y, z))), None)
            square(sx * scale + gap * 2 + z * scale, base + (sy - 1 - y) * scale, material)
    return ("\n".join(svg) + "\n</svg>\n").encode("utf-8")


def preview_boxes(material):
    """Local cuboids for the supported block states; schematic, not game textures."""
    detail = DETAILS.get(material, {})
    shape, props = detail.get("shape", "cube"), detail.get("properties", {})
    if shape == "slab":
        return [(0, 0 if props["type"] == "bottom" else .5, 0,
                 1, .5 if props["type"] == "bottom" else 1, 1)]
    if shape == "stairs":
        upper = {"north": (0, .5, 0, 1, 1, .5), "south": (0, .5, .5, 1, 1, 1),
                 "east": (.5, .5, 0, 1, 1, 1), "west": (0, .5, 0, .5, 1, 1)}
        return [(0, 0, 0, 1, .5, 1), upper[props["facing"]]]
    if shape == "shutter":
        return [{"north": (0, 0, 0, 1, 1, .1875), "south": (0, 0, .8125, 1, 1, 1),
                 "east": (.8125, 0, 0, 1, 1, 1), "west": (0, 0, 0, .1875, 1, 1)}[props["facing"]]]
    if shape == "door":
        return [(0, 0, .8125, 1, 1, 1)]
    if shape == "lantern":
        return [(.31, .12, .31, .69, .65, .69), (.25, .65, .25, .75, .78, .75),
                (.44, .78, .44, .56, 1, .56)]
    if shape == "post":
        return [(.375, 0, .375, .625, 1, .625)]
    if shape == "bush":
        return [(.1, 0, .1, .9, .7, .9)]
    if shape == "flower":
        return [(.43, 0, .43, .57, .6, .57), (.2, .5, .2, .8, .8, .8)]
    if shape == "carpet":
        return [(0, 0, 0, 1, .0625, 1)]
    if shape == "path":
        return [(0, 0, 0, 1, .9375, 1)]
    return [(0, 0, 0, 1, 1, 1)]


def preview_svg(volume):
    """Isometric view of final geometry, including stairs/slabs and oriented details."""
    import math
    sx, sy, sz = volume["size"]
    unit, pad = 18, 56
    def project(point):
        x, y, z = point
        return ((x + z) * unit, (x - z) * unit * .5 - y * unit)
    corners = [project((x, y, z)) for x in (0, sx) for y in (0, sy) for z in (0, sz)]
    minx, miny = min(p[0] for p in corners), min(p[1] for p in corners)
    width = math.ceil(max(p[0] for p in corners) - minx + pad * 2)
    height = math.ceil(max(p[1] for p in corners) - miny + pad * 2)
    def screen(point):
        x, y = project(point)
        return (x - minx + pad, y - miny + pad)
    def material_at(x, y, z):
        if not (0 <= x < sx and 0 <= y < sy and 0 <= z < sz):
            return None
        i = volume["cells"][(x * sy + y) * sz + z]
        return volume["palette"][i] if i >= 0 and volume["palette"][i] != "air" else None
    def opaque(material):
        return material and material != "glass" and DETAILS.get(material, {}).get("shape", "cube") == "cube"
    def shade(color, factor):
        channels = [max(0, min(255, round(int(color[i:i+2], 16) * factor))) for i in (1, 3, 5)]
        return "#" + "".join(f"{c:02x}" for c in channels)
    faces = []
    for (x, y, z), state in positions(volume):
        material = volume["palette"][state]
        if material == "air":
            continue
        for a, b, c, d, e, f in preview_boxes(material):
            a, b, c, d, e, f = a+x, b+y, c+z, d+x, e+y, f+z
            candidates = [
                ("top", [(a,e,c),(d,e,c),(d,e,f),(a,e,f)], e==y+1, (x,y+1,z), 1.10),
                ("front", [(a,b,c),(d,b,c),(d,e,c),(a,e,c)], c==z, (x,y,z-1), .96),
                ("right", [(d,b,c),(d,b,f),(d,e,f),(d,e,c)], d==x+1, (x+1,y,z), .72)]
            for face, points, boundary, neighbor, lighting in candidates:
                if boundary and opaque(material_at(*neighbor)):
                    continue
                color = MATERIALS[material][2]
                if material == "grass_block" and face != "top":
                    color = "#897451"
                variation = .97 + ((x*73+y*37+z*19) % 9) * .007
                depth = sum(p[0] + p[1] - p[2] for p in points) / 4
                faces.append((depth, face, [screen(p) for p in points],
                              shade(color, lighting*variation), material))
    if faces:
        all_points = [point for row in faces for point in row[2]]
        left, top = min(p[0] for p in all_points), min(p[1] for p in all_points)
        width = math.ceil(max(p[0] for p in all_points) - left + pad*2)
        height = math.ceil(max(p[1] for p in all_points) - top + pad*2)
        faces = [(depth, face, [(x-left+pad,y-top+pad) for x,y in points], color, material)
                 for depth,face,points,color,material in faces]
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
           '<rect width="100%" height="100%" fill="#f1eee5"/>',
           '<text x="32" y="28" font-family="sans-serif" font-size="15" fill="#425047">Aldeano · vista isometrica de la geometria exportada</text>']
    def line(p, q, opacity=".18"):
        svg.append(f'<line x1="{p[0]:.2f}" y1="{p[1]:.2f}" x2="{q[0]:.2f}" y2="{q[1]:.2f}" stroke="#1c2927" stroke-opacity="{opacity}" stroke-width=".6"/>')
    def lerp(a, b, t):
        return (a[0] + (b[0]-a[0])*t, a[1] + (b[1]-a[1])*t)
    for _, face, points, color, material in sorted(faces, key=lambda row: row[0]):
        coords = " ".join(f"{p[0]:.2f},{p[1]:.2f}" for p in points)
        opacity = '.62' if material == 'glass' else '1'
        svg.append(f'<polygon points="{coords}" fill="{color}" fill-opacity="{opacity}" stroke="#26302b" stroke-opacity=".13" stroke-width=".5"/>')
        if face != "top" and any(word in material for word in ("planks", "brick", "stone", "log")):
            if "log_y" in material:
                for t in (.23, .72):
                    line(lerp(points[0],points[1],t),lerp(points[3],points[2],t))
            else:
                for t in ((.5,) if "brick" in material else (.33,.67)):
                    line(lerp(points[0],points[3],t),lerp(points[1],points[2],t))
                if "brick" in material:
                    line(lerp(points[0],points[1],.5),lerp(points[3],points[2],.5))
    svg.append("</svg>\n")
    return "\n".join(svg).encode("utf-8")


def analyze_quality(volume):
    """Diagnostics for review, not an aesthetic score or a game physics simulation."""
    sx, sy, sz = volume["size"]
    cells, palette = volume["cells"], volume["palette"]
    counts = Counter(palette[n] for n in cells if n >= 0)
    def solid(x, y, z):
        idx = cells[(x*sy+y)*sz+z]
        return idx >= 0 and palette[idx] != "air"
    covered = 0
    for x in range(sx):
        for z in range(sz):
            highest = next((y for y in range(sy-1,-1,-1) if solid(x,y,z)), -1)
            for y in range(1, highest-1):
                if solid(x,y-1,z) and not solid(x,y,z) and not solid(x,y+1,z):
                    covered += 1
    warnings = []
    if counts.get("air", 0) == 0:
        warnings.append("Sin vaciado explicito: comprueba interiores y terreno existente.")
    if len(counts) < 4:
        warnings.append("Paleta reducida: revisa contraste, marco y cubierta si buscas detalle.")
    if covered < 4:
        warnings.append("Poco espacio cubierto con dos celdas libres; puede ser correcto en un puente.")
    return {"kind": "diagnostics_not_aesthetic_score", "materials_used": len(counts),
            "covered_two_cell_spaces": covered, "explicit_air": counts.get("air", 0),
            "warnings": warnings, "visual_review_required": True,
            "limitations": "Las celdas parciales, puertas y vegetacion no se simulan como fisica del juego."}



def validate_components(volume):
    sx, sy, sz = volume["size"]
    def at(x, y, z):
        if not (0 <= x < sx and 0 <= y < sy and 0 <= z < sz):
            return None
        state = volume["cells"][(x*sy+y)*sz+z]
        return volume["palette"][state] if state >= 0 else None
    pairs = 0
    for (x,y,z), state in positions(volume):
        material = volume["palette"][state]
        if material == "spruce_door_lower":
            if at(x,y+1,z) != "spruce_door_upper":
                _fail(f"Puerta en {[x,y,z]}: falta la mitad superior en Y+1.")
            pairs += 1
        elif material == "spruce_door_upper" and at(x,y-1,z) != "spruce_door_lower":
            _fail(f"Puerta en {[x,y,z]}: falta la mitad inferior en Y-1.")
    return pairs


def generate(build, edition=None, java_profile=DEFAULT_JAVA_PROFILE, max_size=32,
             pack_version=(1, 0, 0), delivery="full"):
    if delivery not in DELIVERIES:
        _fail("Entrega desconocida.")
    required = {"mcstructure": "bedrock", "nbt": "java", "structures": "both"}.get(delivery)
    edition = edition or required or "both"
    if required and edition != required:
        _fail(f"La entrega {delivery} requiere --edition {required}.")
    request = None
    if type(build) is dict and build.get("schema") == "aldeano-architecture/v1":
        request = build
        try:
            from architect import build_architecture
            build = build_architecture(request)
        except (ImportError, ValueError) as error:
            _fail(f"No se puede crear la arquitectura: {error}")
    validate_build(build, max_size)
    if edition not in ("both", "bedrock", "java") or java_profile not in JAVA_PROFILES:
        _fail("Edicion o perfil desconocido.")
    if (len(pack_version) != 3 or any(type(n) is not int or not 0 <= n <= 65535
                                    for n in pack_version)):
        _fail("Version del pack: tres enteros entre 0 y 65535.")
    volume, outputs = compile_volume(build), {}
    door_pairs = validate_components(volume)
    name = build["name"]
    if edition in ("bedrock", "both"):
        structure = export_mcstructure(volume)
        outputs[name + ".mcstructure"] = structure
        outputs[name + ".mcpack"] = package_bedrock(structure, name, pack_version)
    if edition in ("java", "both"):
        structure = export_java_structure(volume, java_profile)
        outputs[name + ".nbt"] = structure
        outputs[name + ".datapack.zip"] = package_java(structure, name, java_profile)
    checks = validate_outputs(outputs, volume, name, edition, java_profile)
    checks += ["typed_structure_schema", "paired_door_halves"]
    if edition != "bedrock":
        checks += ["java_gzip_crc32", "java_profile_match"]
    counts = Counter(volume["palette"][i] for i in volume["cells"] if i >= 0)
    report = {
        "generator_version": VERSION, "schema": SCHEMA, "name": name,
        "edition": edition, "delivery": delivery,
        "java_profile": java_profile if edition != "bedrock" else None,
        "bedrock_profile": "bedrock-1.26.30" if edition != "java" else None,
        "pack_version": list(pack_version), "size": volume["size"],
        "door_pairs": door_pairs,
        "placed_blocks": sum(counts.values()) - counts.get("air", 0),
        "explicit_air": counts.get("air", 0), "omitted_cells": volume["cells"].count(-1),
        "validation": {"level": "structural", "passed": True, "checks": checks,
                       "minecraft_tested": False},
        "sha256": {key: hashlib.sha256(value).hexdigest() for key, value in outputs.items()},
    }
    if delivery != "full":
        extensions = {"mcstructure": (".mcstructure",), "nbt": (".nbt",),
                      "structures": (".mcstructure", ".nbt")}[delivery]
        outputs = {key: value for key, value in outputs.items() if key.endswith(extensions)}
        report["sha256"] = {key: hashlib.sha256(value).hexdigest() for key, value in outputs.items()}
        report["review"] = analyze_quality(volume)
        return outputs, report
    outputs[name + ".build.json"] = _json(build)
    if request is not None:
        outputs[name + ".request.json"] = _json(request)
    outputs["revision.json"] = _json(analyze_quality(volume))
    outputs["validacion.json"] = _json(report)
    outputs["materiales.txt"] = ("\n".join(f"{m}: {n}" for m, n in sorted(counts.items())
                                         if m != "air") + "\n").encode("utf-8")
    outputs["preview.svg"] = preview_svg(volume)
    outputs["preview_planos.svg"] = preview_ortho_svg(volume)
    help_text = f"""Aldeano Build Generator {VERSION} - {name}
Validacion estructural correcta. No se ha probado esta construccion dentro del juego.
Edicion solicitada: {edition}. Java: {java_profile}. Bedrock: motor minimo 1.26.30.

BEDROCK WINDOWS: /give @s structure_block
Bloque de estructura > Cargar > Importar > seleccionar {name}.mcstructure > Cargar.
ALTERNATIVA BEDROCK: abrir {name}.mcpack con Minecraft, activar el pack en el mundo.
Con permisos de comandos: /structure load aldeano:{name} ~ ~ ~
La importacion del archivo de estructura desde su boton requiere Windows y ser anfitrion.
Movil: asociacion del mcpack pendiente de prueba por plataforma. Consola sin ruta directa.

JAVA: copiar {name}.datapack.zip a datapacks/ dentro de la carpeta del mundo.
No extraerlo ni copiar el ZIP general. Cargar el mundo o ejecutar /reload.
Con permisos de comandos: /place template aldeano:{name} ~ ~ ~
El datapack debe corresponder a la version Java elegida al generar.
NBT SUELTO: copiar {name}.nbt a generated/aldeano/structures/ dentro del mundo.
En un bloque de estructura Java, modo Cargar, usar aldeano:{name}.
No es un schematic de WorldEdit ni un archivo de Litematica.

Las posiciones omitidas conservan el mundo; el aire explicito vacia posiciones.
Para pruebas, usa un mundo creativo de ensayo con espacio libre y permisos.
Si actualizas el mismo pack Bedrock, incrementa --pack-version (ejemplo: 1.0.1).
Conserva el .build.json o .request.json para revisiones. preview.svg muestra una vista 3D.
preview_planos.svg contiene las tres proyecciones. revision.json incluye comprobaciones orientativas.
"""
    outputs["LEEME.txt"] = help_text.encode("utf-8")
    outputs[name + ".todo.zip"] = _zip(outputs)
    return outputs, report


def write_outputs(outputs, destination, overwrite=False):
    """Stage, read back, verify, then atomically replace each individual file."""
    destination = Path(destination)
    conflicts = [name for name in outputs if (destination / name).exists()]
    if conflicts and not overwrite:
        _fail("Ya existen archivos de salida. Usa otra carpeta o --overwrite: " + ", ".join(conflicts))
    destination.mkdir(parents=True, exist_ok=True)
    staged = []
    try:
        for name, contents in outputs.items():
            if Path(name).name != name:
                _fail("Nombre de archivo de salida no valido.")
            with tempfile.NamedTemporaryFile(dir=destination, suffix=".tmp", delete=False) as stream:
                temporary = Path(stream.name)
                staged.append((temporary, destination / name, contents))
                stream.write(contents)
                stream.flush()
                os.fsync(stream.fileno())
            saved = temporary.read_bytes()
            if saved != contents:
                _fail(f"Escritura incompleta de {name}; no se entrega.")
            if name.endswith((".nbt", ".mcstructure")):
                verify_structure(saved, name.rsplit(".", 1)[1])
            elif name.endswith((".zip", ".mcpack")):
                with zipfile.ZipFile(io.BytesIO(saved)) as archive:
                    if archive.testzip() is not None:
                        _fail(f"CRC incorrecto en {name}.")
        for temporary, target, contents in staged:
            os.replace(temporary, target)
            if target.read_bytes() != contents:
                _fail(f"La lectura final de {target.name} no coincide; no se entrega.")
    finally:
        for temporary, _, _ in staged:
            temporary.unlink(missing_ok=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Construcciones Bedrock y Java desde BuildSpec.")
    parser.add_argument("input", nargs="?", help="JSON del diseno; no es un archivo NBT.")
    parser.add_argument("--edition", choices=("both", "bedrock", "java"))
    parser.add_argument("--java-profile", choices=tuple(JAVA_PROFILES))
    parser.add_argument("--delivery", choices=DELIVERIES, default="full",
                        help="Solo el formato solicitado o paquete completo.")
    parser.add_argument("--verify", metavar="ARCHIVO", help="Verificar una estructura ya guardada.")
    parser.add_argument("--output", default="output")
    parser.add_argument("--max-size", type=int, choices=(32, 48), default=32)
    parser.add_argument("--pack-version", default="1.0.0")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--catalog", action="store_true")
    parser.add_argument("--version", action="version", version=VERSION)
    args = parser.parse_args(argv)
    try:
        if args.verify:
            if args.input:
                _fail("Usa --verify sin JSON de entrada.")
            path = Path(args.verify)
            if path.stat().st_size > MAX_NBT_BYTES:
                _fail("La estructura supera el limite de verificacion.")
            result = verify_structure(path.read_bytes(), path.suffix.lstrip("."), args.java_profile)
            print(json.dumps({"ok": True, "file": str(path), "verification": result}, indent=2))
            return 0
        if args.catalog:
            print(json.dumps({"materials": list(MATERIALS), "java_profiles": JAVA_PROFILES,
                              "bedrock_engine": BEDROCK_ENGINE}, indent=2))
            return 0
        if not args.input:
            parser.error("Indica un JSON de entrada o utiliza --catalog.")
        edition = args.edition or {"mcstructure": "bedrock", "nbt": "java", "structures": "both"}.get(args.delivery, "both")
        if edition != "bedrock" and args.java_profile is None:
            _fail("Indica --java-profile java-1.21.1 o java-26.3 segun tu version; no se presupone la mas reciente.")
        source = Path(args.input)
        if source.stat().st_size > MAX_BYTES:
            _fail("El archivo de entrada supera 256 KiB.")
        build = parse_build(source.read_text(encoding="utf-8-sig"))
        if not re.fullmatch(r"\d{1,5}\.\d{1,5}\.\d{1,5}", args.pack_version):
            _fail("--pack-version debe tener forma 1.0.0.")
        pack_version = tuple(map(int, args.pack_version.split(".")))
        outputs, report = generate(build, edition, args.java_profile or DEFAULT_JAVA_PROFILE,
                                   args.max_size, pack_version, args.delivery)
        destination = Path(args.output)
        write_outputs(outputs, destination, args.overwrite)
        print(json.dumps({"ok": True, "files": [str(destination / n) for n in outputs],
                          "java_profile": report["java_profile"], "delivery": args.delivery,
                          "sha256": report["sha256"],
                          "validation": dict(report["validation"], disk_readback=True),
                          "review": report.get("review")}, ensure_ascii=False, indent=2))
        return 0
    except (BuildError, OSError, UnicodeError, OverflowError, zipfile.BadZipFile) as error:
        print(json.dumps({"ok": False, "error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
