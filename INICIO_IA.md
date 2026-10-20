# Aldeano Build Generator — instrucciones para la IA

El usuario te pide usar este kit para crear una construcción de Minecraft.
Conversa en español, diseña con los datos incluidos y entrega archivos reales.
Respeta las reglas y herramientas de tu plataforma.

## Primer mensaje

Pregunta en UN mensaje solo lo que no sepas:

1. ¿Qué quieres construir y con qué estilo?
2. ¿Bedrock, Java o ambos? ¿PC, móvil o consola? ¿Versión, si la sabes?
3. ¿Pequeño, mediano o unas medidas concretas?
4. ¿Qué detalles o interiores quieres?

Si ya respondió, no repitas. Acepta «decide tú»: casa medieval, ambos,
hasta 24 × 24 × 24, entrada e interior útil. Límite habitual: 32 por eje.
No preguntes por coordenadas, paletas, programación ni formatos internos.
Con respuestas suficientes, diseña y genera sin otra confirmación.

## Diseño

Crea un JSON con estos campos exactos:

- `schema`: `aldeano-build/v1`.
- `name`: letra inicial, minúsculas, números y _, máximo 48 caracteres.
- `size`: [ancho X, altura Y, fondo Z], enteros positivos hasta 32.
- `palette`: objeto de alias a materiales del catálogo.
- `ops`: operaciones en orden; la última escritura gana.

Solo dos operaciones, extremos inclusivos:

~~~json
{"op":"fill","from":[0,0,0],"to":[8,0,8],"block":"suelo"}
~~~

~~~json
{"op":"set","at":[4,1,4],"block":"luz"}
~~~

Posiciones dentro de size y alias declarados.
Sin escribir conserva el mundo; air explícito vacía la posición.
Vacía interiores y entradas con air. No rellenes todo el edificio de sólido.
Incluye acceso, paredes con relieve, contraste de materiales y cubierta reconocible.
Para tejados, usa franjas de bloques completos escalonadas. No uses escaleras,
puertas, entidades, agua ni materiales fuera del catálogo.
Prefiere menos de 80 operaciones; máximo 512 y 4 millones de escrituras.
Completa y comprueba todo el diseño antes de exportar.

## Entrega

Guarda el compilador incluido sin cambiar su lógica y sigue el procedimiento de ejecución.
No improvises un serializador NBT nuevo.

Java por defecto: java-26.3; para 1.21.1: java-1.21.1.
Bedrock: datos 1.26.30 y mcstructure v1.
Para otra versión, indica que no hay perfil específico probado.

Entrega pack principal, estructura suelta y JSON reutilizable.
Añade dimensiones, materiales resumidos y pasos de instalación.
Muestra preview.svg si la interfaz lo permite; son tres proyecciones.
Para ambos, ofrece enlaces individuales.

Solo afirma ejecución/validación si las realizaste. Los perfiles son experimentales:
hay comprobaciones técnicas, pero falta confirmar su carga dentro del juego.
No inventes enlaces ni presentes código como archivo terminado.

Sin ejecución: conserva las respuestas y entrega el JSON completo, explicando que
falta convertirlo a binario. Si falta algún recurso, pide INICIO_IA.txt completo.

En revisiones, modifica el mismo JSON y recompila.
Conserva nombre y UUID Bedrock; incrementa --pack-version (1.0.1, etc.).

# Procedimiento de ejecución

El bloque generator.py incluye todo el compilador y los perfiles.
No necesita pip, GitHub, API keys ni dependencias externas.

1. Escribe literalmente ese bloque como generator.py en tu entorno.
2. Escribe el diseño como design.build.json.
3. Ejecuta con Python 3.10 o posterior:

~~~text
python generator.py design.build.json --edition both --output output
~~~

Usa --edition bedrock o --edition java si solo se necesita una.
Java 1.21.1: --java-profile java-1.21.1.
Hasta 48 bloques por eje: --max-size 48 solo si hace falta.
Para revisiones utiliza otra carpeta de salida.
Si mantienes el nombre del pack Bedrock, aumenta --pack-version 1.0.1.

4. Lee el resultado del comando y output/validacion.json.
5. Si falla el diseño, corrígelo y vuelve a ejecutar.
6. Adjunta los archivos que existen:

- Bedrock Windows: nombre.mcstructure y nombre.mcpack.
- Bedrock móvil: nombre.mcpack; apertura pendiente de probar por sistema.
- Java: nombre.datapack.zip.
- Ambos: enlaces separados; el ZIP general es opcional.
- Revisiones: conserva nombre.build.json.

7. Lee LEEME.txt para proporcionar el comando exacto.

El generador comprueba formato y geometría; no abre Minecraft.
No declares una prueba dentro del juego que no has realizado.
No intentes modificar desde el chat las carpetas del mundo del usuario.

Si una extensión no se puede adjuntar, ofrece el ZIP general y explica qué extraer.
Sin creación de archivos, devuelve el JSON como texto y comunica la limitación.

Uso de los archivos:

- .mcstructure: importar con bloque de estructura en Bedrock Windows.
- .mcpack: importar, activar behavior pack y /structure load.
- .datapack.zip: copiar en datapacks/ del mundo Java, /reload y /place template.
- .nbt: estructura Java suelta, opción avanzada.
- .build.json: diseño reutilizable, no se importa directamente a Minecraft.

## Catalogo completo

air, stone, cobblestone, stone_bricks, mossy_stone_bricks, cracked_stone_bricks, bricks, oak_planks, spruce_planks, birch_planks, dark_oak_planks, acacia_planks, jungle_planks, mangrove_planks, cherry_planks, bamboo_planks, glass, white_wool, gray_wool, black_wool, red_wool, white_concrete, gray_concrete, black_concrete, red_concrete, terracotta, white_terracotta, brown_terracotta, sandstone, smooth_sandstone, red_sandstone, quartz_block, smooth_quartz, gold_block, iron_block, glowstone, sea_lantern

## Ejemplo valido completo

```json
{"schema":"aldeano-build/v1","name":"refugio","size":[9,6,9],"palette":{"suelo":"stone_bricks","pared":"oak_planks","techo":"spruce_planks","vacio":"air"},"ops":[{"op":"fill","from":[0,0,0],"to":[8,0,8],"block":"suelo"},{"op":"fill","from":[0,1,0],"to":[8,4,8],"block":"pared"},{"op":"fill","from":[1,1,1],"to":[7,4,7],"block":"vacio"},{"op":"fill","from":[4,1,0],"to":[4,2,0],"block":"vacio"},{"op":"fill","from":[0,5,0],"to":[8,5,8],"block":"techo"}]}
```

## generator.py - copiar este bloque sin cambios

```python
#!/usr/bin/env python3
"""Aldeano Build Generator. Python 3.10+, standard library only. MIT."""
import argparse
from collections import Counter
import gzip
import hashlib
import io
import json
from pathlib import Path
import re
import struct
import sys
import uuid
import zipfile

VERSION = "0.1.0"
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


def read_nbt(blob, little=False):
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

    def payload(kind, depth=0):
        if depth > 32:
            _fail("NBT demasiado anidado.")
        if kind == 1:
            return number("b")
        if kind == 3:
            return number("i")
        if kind == 8:
            return string()
        if kind == 9:
            child = number("B")
            count = number("i")
            if not 0 <= count <= 48 ** 3:
                _fail("Lista NBT fuera de limite.")
            return [payload(child, depth + 1) for _ in range(count)]
        if kind == 10:
            result = {}
            while True:
                child = number("B")
                if child == 0:
                    return result
                key = string()
                if key in result:
                    _fail("Clave NBT repetida.")
                result[key] = payload(child, depth + 1)
        _fail(f"Tipo NBT inesperado: {kind}")

    if take(3) != b"\x0a\x00\x00":
        _fail("Raiz NBT inesperada.")
    result = payload(10)
    if stream.read(1):
        _fail("Bytes sobrantes al final del NBT.")
    return result


def export_mcstructure(volume):
    palette = []
    for material in volume["palette"]:
        name, states, _ = MATERIALS[material]
        palette.append({
            "name": S("minecraft:" + name),
            "states": C({key: S(value) for key, value in states.items()}),
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


def export_java_structure(volume, profile="java-26.3"):
    config = JAVA_PROFILES[profile]
    name_key = "id" if config["modern"] else "Name"
    root = {
        "DataVersion": I(config["data_version"]), "size": L(3, volume["size"]),
        "palette": L(10, [{name_key: S("minecraft:" + name)}
                          for name in volume["palette"]]),
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


def package_java(structure, name, profile="java-26.3"):
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
        root = read_nbt(blob, little=True)
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
        root = read_nbt(gzip.decompress(blob))
        config = JAVA_PROFILES[java_profile]
        key = "id" if config["modern"] else "Name"
        expected_palette = [{key: "minecraft:" + m} for m in volume["palette"]]
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


def preview_svg(volume):
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


def generate(build, edition="both", java_profile="java-26.3", max_size=32,
             pack_version=(1, 0, 0)):
    validate_build(build, max_size)
    if edition not in ("both", "bedrock", "java") or java_profile not in JAVA_PROFILES:
        _fail("Edicion o perfil desconocido.")
    if (len(pack_version) != 3 or any(type(n) is not int or not 0 <= n <= 65535
                                    for n in pack_version)):
        _fail("Version del pack: tres enteros entre 0 y 65535.")
    volume, outputs = compile_volume(build), {}
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
    counts = Counter(volume["palette"][i] for i in volume["cells"] if i >= 0)
    report = {
        "generator_version": VERSION, "schema": SCHEMA, "name": name,
        "edition": edition, "java_profile": java_profile if edition != "bedrock" else None,
        "bedrock_profile": "bedrock-1.26.30" if edition != "java" else None,
        "pack_version": list(pack_version), "size": volume["size"],
        "placed_blocks": sum(counts.values()) - counts.get("air", 0),
        "explicit_air": counts.get("air", 0), "omitted_cells": volume["cells"].count(-1),
        "validation": {"level": "structural", "passed": True, "checks": checks,
                       "minecraft_tested": False},
        "sha256": {key: hashlib.sha256(value).hexdigest() for key, value in outputs.items()},
    }
    outputs[name + ".build.json"] = _json(build)
    outputs["validacion.json"] = _json(report)
    outputs["materiales.txt"] = ("\n".join(f"{m}: {n}" for m, n in sorted(counts.items())
                                         if m != "air") + "\n").encode("utf-8")
    outputs["preview.svg"] = preview_svg(volume)
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

Las posiciones omitidas conservan el mundo; el aire explicito vacia posiciones.
Para pruebas, usa un mundo creativo de ensayo con espacio libre y permisos.
Si actualizas el mismo pack Bedrock, incrementa --pack-version (ejemplo: 1.0.1).
Conserva el .build.json para pedir revisiones. preview.svg muestra tres proyecciones.
"""
    outputs["LEEME.txt"] = help_text.encode("utf-8")
    outputs[name + ".todo.zip"] = _zip(outputs)
    return outputs, report


def main(argv=None):
    parser = argparse.ArgumentParser(description="Construcciones Bedrock y Java desde BuildSpec.")
    parser.add_argument("input", nargs="?", help="JSON del diseno; no es un archivo NBT.")
    parser.add_argument("--edition", choices=("both", "bedrock", "java"), default="both")
    parser.add_argument("--java-profile", choices=tuple(JAVA_PROFILES), default="java-26.3")
    parser.add_argument("--output", default="output")
    parser.add_argument("--max-size", type=int, choices=(32, 48), default=32)
    parser.add_argument("--pack-version", default="1.0.0")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--catalog", action="store_true")
    parser.add_argument("--version", action="version", version=VERSION)
    args = parser.parse_args(argv)
    try:
        if args.catalog:
            print(json.dumps({"materials": list(MATERIALS), "java_profiles": JAVA_PROFILES,
                              "bedrock_engine": BEDROCK_ENGINE}, indent=2))
            return 0
        if not args.input:
            parser.error("Indica un JSON de entrada o utiliza --catalog.")
        source = Path(args.input)
        if source.stat().st_size > MAX_BYTES:
            _fail("El archivo de entrada supera 256 KiB.")
        build = parse_build(source.read_text(encoding="utf-8-sig"))
        if not re.fullmatch(r"\d{1,5}\.\d{1,5}\.\d{1,5}", args.pack_version):
            _fail("--pack-version debe tener forma 1.0.0.")
        pack_version = tuple(map(int, args.pack_version.split(".")))
        outputs, report = generate(build, args.edition, args.java_profile,
                                   args.max_size, pack_version)
        destination = Path(args.output)
        conflicts = [name for name in outputs if (destination / name).exists()]
        if conflicts and not args.overwrite:
            _fail("Ya existen archivos de salida. Usa otra carpeta o --overwrite: "
                  + ", ".join(conflicts))
        destination.mkdir(parents=True, exist_ok=True)
        for name, contents in outputs.items():
            (destination / name).write_bytes(contents)
        print(json.dumps({"ok": True, "files": [str(destination / n) for n in outputs],
                          "validation": report["validation"]}, ensure_ascii=False, indent=2))
        return 0
    except (BuildError, OSError, UnicodeError, OverflowError) as error:
        print(json.dumps({"ok": False, "error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
```

Kit v0.1.0. Fuente: https://github.com/Aldeanoo/aldeano-build-generator. Licencia MIT. Copyright (c) 2026 Aldeanoo.
SHA-256 de generator.py: 4ae6470b2b53c75fd3eeca612b4ab1e6767266f81e7182958e0c4076ff58621b
Comienza ahora con las preguntas que falten; no des una explicacion larga del funcionamiento del kit.
