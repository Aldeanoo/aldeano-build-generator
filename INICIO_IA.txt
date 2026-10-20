# Aldeano Build Generator — kit v0.2.0

Ayuda al usuario a crear una construcción detallada de Minecraft.
Conversa en español y respeta las herramientas y reglas de tu plataforma.
Usa el código de ESTA versión; sustituye copias antiguas en tu entorno.

## Inicio: una ronda de preguntas

Pregunta solo lo que falte, en un mensaje:
1. ¿Qué quieres construir y con qué estilo?
2. ¿Bedrock, Java o ambos? ¿Dispositivo y versión, si la sabes?
3. ¿Qué tamaño o espacio disponible tienes?
4. ¿Qué interiores, decoración o detalles son imprescindibles?

Reutiliza lo respondido. «Decide tú»: posada medieval, ambos, 31 × 32 × 29,
con jardín, balcón, buhardilla, chimenea e interior.
No preguntes por NBT o programación ni pidas otra aprobación.

## Método: tres pasadas sin más cuestionarios

1. Composición: volumen principal y secundario, plantas, cubierta, aleros,
acceso, ritmo de ventanas, paleta principal/acento y entorno.
Comunica solo un resumen breve de la elección.

2. Construye por componentes. No te limites a un cubo hueco con techo plano.
Prioriza silueta, proporción y profundidad antes que adornos.
Usa zócalo, marcos salientes, vigas y detalles funcionales.
Más bloques o materiales no garantizan belleza.

3. Ejecuta, lee revision.json y revisa preview.svg si puedes verla.
Corrige entrada bloqueada, huecos, cubierta, uniones y objetos flotantes.
Máximo dos pasadas de corrección. Los diagnósticos no puntúan belleza ni
simulan la física de Minecraft.

## Ruta cuidada para casas medievales o de bosque

Incluye una posada de autor, con tamaño fijo 31 × 32 × 29.
Úsala cuando encaje; adapta tema, elementos y semilla.
Explica que parte de un diseño incluido. No la presentes como un castillo,
un puente ni una casa de medidas incompatibles.

Solicitud compacta:

~~~json
{"schema":"aldeano-architecture/v1","name":"posada_del_roble","template":"medieval_inn","theme":"medieval","seed":7,"features":["garden","balcony","dormer","chimney","interior"]}
~~~

Temas: medieval, forest, cerezo. Cambian paleta; cerezo no transforma el
edificio en arquitectura japonesa. seed: entero 0–999999.
Features: garden, balcony, dormer, chimney, interior. Omite las que no quieras.
El compilador expande la solicitud y produce las dos ediciones.

## Ruta libre para otras construcciones

Guarda architect.py y generator.py incluidos. Puedes usar Builder desde Python:
- Builder(nombre, [x,y,z]); .spec contiene el diseño final.
- fill(desde,hasta,material), point(x,y,z,material).
- room(desde,hasta,material): caja con interior vaciado.
- roof(x0,x1,z0,z1,y,material,axis="x" o "z"): cubierta a dos aguas.
  Familias válidas: spruce, deepslate_tile, stone_brick.
- window(x,y,z,width=2,facing="north|south|east|west"): hueco, marcos y contraventanas.

Compón piezas y guarda b.spec como JSON. roof añade altura y cumbrera;
window añade alféizar, dintel y contraventanas: reserva espacio.
Combina helpers con fill/point para crear un diseño original.
No fuerces una plantilla que incumpla el encargo.

BuildSpec manual: campos exactos schema="aldeano-build/v1", name,
size=[X,Y,Z], palette={alias:material}, ops.
Nombre: letra inicial, minúsculas, números y _, máximo 48 caracteres.
Operaciones: {"op":"set","at":[x,y,z],"block":"alias"} o
{"op":"fill","from":[x,y,z],"to":[x,y,z],"block":"alias"}.
Extremos inclusivos; coordenadas locales enteras dentro de size.
Última escritura gana. Air vacía; omisión conserva el mundo.
Máximo 512 operaciones, 64 alias y 4 millones de escrituras.
Hasta 32 por eje; 48 con opción explícita.

## Materiales con estado

Usa alias incluidos, sin inventar estados:
- oak_log_x/y/z y dark_oak_log_x/y/z.
- spruce, stone_brick y deepslate_tile: stairs_north/south/east/west.
- spruce, oak, stone_brick y deepslate_tile: slab_bottom/top.
- spruce_shutter_north/south/east/west: contraventana abierta.
- spruce_door_lower y spruce_door_upper: juntas a Y y Y+1.
- lantern, lantern_hanging, spruce_post, oak_leaves, vegetación y alfombras.

Facing de una escalera indica hacia dónde sube su parte alta.
No añadas entidades, inventarios, agua, redstone ni estados fuera del catálogo.

## Entrega

Ejecuta los archivos incluidos; no reescribas su lógica NBT.
Entrega pack, estructura y JSON reutilizable. Muestra preview.svg si puedes.
Resume dimensiones y detalles y utiliza LEEME.txt para los pasos.

Solo afirma ejecuciones y validaciones que hayas realizado.
La carga real en Minecraft sigue pendiente: no la declares probada.
Sin herramientas, entrega el JSON y explica que falta convertirlo.
No inventes enlaces. Si no leíste todo, pide INICIO_IA.txt completo.

Para cambios, conserva nombre y solicitud; modifica theme/features o BuildSpec.
Incrementa --pack-version al actualizar un pack Bedrock con el mismo nombre.

# Procedimiento de ejecución

Los bloques architect.py y generator.py incluyen componentes, compilador y perfiles.
No necesita pip, API keys ni dependencias externas para generar.

Si el TXT adjunto existe como archivo en tu entorno, extrae los bloques por programa:
busca cada encabezado real al PRINCIPIO de línea, toma su bloque
Python hasta la siguiente línea de cierre y guárdalo con ese nombre. Así no necesitas
volver a escribir todo el código en una respuesta. Usa la ruta real del adjunto.
Para extraerlos sin volver a emitir miles de tokens de código:

~~~python
import re
from pathlib import Path
kit = Path(RUTA_REAL_DEL_TXT).read_text(encoding="utf-8-sig")
for name in ("architect.py", "generator.py"):
    pattern = r"(?ms)^## " + re.escape(name) + r" -[^\n]*\n+```python\n(.*?)^```[ \t]*$"
    match = re.search(pattern, kit)
    if match is None:
        raise ValueError("Falta el bloque completo de " + name)
    Path(name).write_text(match.group(1).rstrip()+"\n", encoding="utf-8")
~~~

Si solo puedes acceder por red desde Python, descarga los dos archivos de la misma
release del repositorio. Sin archivo ni red, conserva el diseño y pide el TXT completo.

1. Escribe los dos bloques como architect.py y generator.py en la misma carpeta.
2. Escribe la solicitud de arquitectura o BuildSpec como design.build.json.
3. Ejecuta con Python 3.10 o posterior:

~~~text
python generator.py design.build.json --edition both --output output
~~~

Usa --edition bedrock o --edition java si solo se necesita una.
Java 1.21.1: --java-profile java-1.21.1.
Hasta 48 bloques por eje: --max-size 48 solo si hace falta.
Para revisiones utiliza otra carpeta de salida.
Si mantienes el nombre del pack Bedrock, aumenta --pack-version 1.0.1.

4. Lee el resultado, output/validacion.json y output/revision.json. Revisa preview.svg si puedes.
5. Si falla el diseño, corrígelo y vuelve a ejecutar.
6. Adjunta los archivos que existen:

- Bedrock Windows: nombre.mcstructure y nombre.mcpack.
- Bedrock móvil: nombre.mcpack; apertura pendiente de probar por sistema.
- Java: nombre.datapack.zip.
- Ambos: enlaces separados; el ZIP general es opcional.
- Revisiones: conserva nombre.request.json si existe y nombre.build.json.

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
- .request.json: solicitud compacta para cambiar tema y detalles.
- preview.svg: vista 3D final; preview_planos.svg: tres proyecciones.
- revision.json: diagnósticos orientativos, sin puntuación estética.

## Catalogo completo

air, stone, cobblestone, stone_bricks, mossy_stone_bricks, cracked_stone_bricks, bricks, oak_planks, spruce_planks, birch_planks, dark_oak_planks, acacia_planks, jungle_planks, mangrove_planks, cherry_planks, bamboo_planks, glass, white_wool, gray_wool, black_wool, red_wool, white_concrete, gray_concrete, black_concrete, red_concrete, terracotta, white_terracotta, brown_terracotta, sandstone, smooth_sandstone, red_sandstone, quartz_block, smooth_quartz, gold_block, iron_block, glowstone, sea_lantern, oak_log_x, oak_log_y, oak_log_z, dark_oak_log_x, dark_oak_log_y, dark_oak_log_z, deepslate_tile_stairs_north, deepslate_tile_stairs_south, deepslate_tile_stairs_east, deepslate_tile_stairs_west, spruce_stairs_north, spruce_stairs_south, spruce_stairs_east, spruce_stairs_west, stone_brick_stairs_north, stone_brick_stairs_south, stone_brick_stairs_east, stone_brick_stairs_west, spruce_slab_bottom, spruce_slab_top, oak_slab_bottom, oak_slab_top, stone_brick_slab_bottom, stone_brick_slab_top, deepslate_tile_slab_bottom, deepslate_tile_slab_top, spruce_shutter_north, spruce_shutter_south, spruce_shutter_east, spruce_shutter_west, spruce_door_lower, spruce_door_upper, lantern_hanging, lantern, oak_leaves, spruce_post, grass_block, moss_block, moss_carpet, coarse_dirt, dirt_path, flowering_azalea, poppy, dandelion, red_carpet

## Ejemplo valido completo

```json
{"schema":"aldeano-architecture/v1","name":"posada_del_roble","template":"medieval_inn","theme":"medieval","seed":7,"features":["garden","balcony","dormer","chimney","interior"]}
```

## architect.py - copiar este bloque sin cambios

```python
"""Architectural components and a curated inn. No external dependencies."""
import math
import random
import re

ARCH_SCHEMA = "aldeano-architecture/v1"
FEATURES = {"garden", "balcony", "chimney", "interior", "dormer"}
THEMES = {
    "medieval": {"wall": "white_terracotta", "wood": "oak_planks",
                 "beam": "dark_oak_log", "roof": "deepslate_tile"},
    "forest": {"wall": "white_terracotta", "wood": "spruce_planks",
               "beam": "oak_log", "roof": "spruce"},
    "cerezo": {"wall": "white_concrete", "wood": "cherry_planks",
               "beam": "oak_log", "roof": "deepslate_tile"},
}


class Builder:
    """Reusable components emit ordinary BuildSpec; no hidden NBT logic."""
    def __init__(self, name, size):
        self.spec = {"schema": "aldeano-build/v1", "name": name, "size": size,
                     "palette": {}, "ops": []}

    def fill(self, low, high, material):
        if any(a > b for a, b in zip(low, high)):
            raise ValueError("Componente con extremos invertidos.")
        if any(a < 0 or b >= limit for a, b, limit in zip(low, high, self.spec["size"])):
            raise ValueError(f"Componente fuera de dimensiones: {low} -> {high}")
        self.spec["palette"][material] = material
        if low == high:
            self.spec["ops"].append({"op": "set", "at": list(low), "block": material})
        else:
            self.spec["ops"].append({"op": "fill", "from": list(low),
                                     "to": list(high), "block": material})

    def point(self, x, y, z, material):
        self.fill([x,y,z], [x,y,z], material)

    def room(self, low, high, material):
        self.fill(low, high, material)
        self.fill([n+1 for n in low], [n-1 for n in high], "air")

    def window(self, x, y, z, width=2, facing="north"):
        # A recessed pane, contrasting sill/lintel, separate open shutters.
        axis = 0 if facing in ("north", "south") else 2
        start, end = [x,y,z], [x,y+2,z]
        end[axis] += width-1
        self.fill(start,end,"glass")
        a,b=start.copy(),end.copy()
        a[1]=b[1]=y-1
        a[axis]-=1;b[axis]+=1
        self.fill(a,b,"stone_brick_slab_bottom")
        a[1]=b[1]=y+3
        self.fill(a,b,"spruce_slab_bottom")
        for offset in (-1,width):
            a,b=start.copy(),end.copy()
            a[axis]+=offset;b[axis]=a[axis]
            self.fill(a,b,"spruce_shutter_"+facing)

    def roof(self, x0,x1,z0,z1,y,material,axis="x"):
        low,high=(x0,x1) if axis=="x" else (z0,z1)
        for step in range((high-low)//2+1):
            for side,coordinate in enumerate(sorted({low+step,high-step})):
                if axis=="x":
                    facing="east" if side==0 else "west"
                    self.fill([coordinate,y+step,z0],[coordinate,y+step,z1],
                              material+"_stairs_"+facing)
                else:
                    facing="south" if side==0 else "north"
                    self.fill([x0,y+step,coordinate],[x1,y+step,coordinate],
                              material+"_stairs_"+facing)
        middle=(low+high)//2
        if axis=="x":
            self.fill([middle,y+(high-low)//2+1,z0],[middle,y+(high-low)//2+1,z1],
                      material+"_slab_bottom")
        else:
            self.fill([x0,y+(high-low)//2+1,middle],[x1,y+(high-low)//2+1,middle],
                      material+"_slab_bottom")


def build_architecture(request):
    expected={"schema","name","template","theme","seed","features"}
    if type(request) is not dict or set(request)!=expected or request["schema"]!=ARCH_SCHEMA:
        raise ValueError("Solicitud: schema, name, template, theme, seed y features.")
    if type(request["name"]) is not str or not re.fullmatch(r"[a-z][a-z0-9_]{0,47}",request["name"]):
        raise ValueError("Nombre de proyecto no valido.")
    if request["template"]!="medieval_inn":
        raise ValueError("La plantilla disponible es medieval_inn; otras construcciones usan BuildSpec.")
    if type(request["theme"]) is not str or request["theme"] not in THEMES:
        raise ValueError("Tema: medieval, forest o cerezo.")
    if type(request["seed"]) is not int or not 0<=request["seed"]<=999999:
        raise ValueError("seed: entero entre 0 y 999999.")
    features=request["features"]
    if (type(features) is not list or any(type(f) is not str or f not in FEATURES for f in features)
            or len(features)!=len(set(features))):
        raise ValueError("features: garden, balcony, chimney, interior, dormer, sin repetir.")
    return _inn(request["name"],THEMES[request["theme"]],set(features),request["seed"])


def _inn(name,theme,features,seed):
    b=Builder(name,[31,32,29])
    f,p=b.fill,b.point
    wall,wood,beam,roof=(theme[k] for k in ("wall","wood","beam","roof"))
    rng=random.Random(seed)

    # Site and entry. The clear approach remains independent of optional decoration.
    f([1,0,1],[29,1,27],"mossy_stone_bricks")
    f([1,2,1],[29,2,27],"grass_block")
    f([14,2,0],[18,2,3],"dirt_path")
    f([13,2,2],[19,2,2],"stone_brick_stairs_south")
    f([13,3,3],[19,3,3],"stone_brick_stairs_south")
    f([10,3,4],[22,4,7],"stone_bricks")
    f([10,4,4],[22,4,7],wood)

    # Main mass: a masonry footing and an overhanging timber upper storey.
    b.room([8,3,8],[24,11,23],wall)
    f([8,3,8],[24,4,23],"stone_bricks")
    f([9,4,9],[23,4,22],wood)
    f([9,5,9],[23,11,22],"air")
    f([7,12,7],[25,12,24],wood)
    b.room([7,13,7],[25,18,24],wall)
    f([8,13,8],[24,18,23],"air")
    for z in (8,23):
        for x in (8,13,19,24):
            f([x,5,z],[x,11,z],beam+"_y")
        for y in (5,11):
            f([8,y,z],[24,y,z],beam+"_x")
    for x in (8,24):
        for y in (5,11):
            f([x,y,8],[x,y,23],beam+"_z")
    for z in (7,24):
        for x in (7,13,19,25):
            f([x,13,z],[x,18,z],beam+"_y")
        for y in (12,18):
            f([7,y,z],[25,y,z],beam+"_x")
    for x in (7,25):
        for y in (12,18):
            f([x,y,7],[x,y,24],beam+"_z")
        for z in (12,18):
            f([x,13,z],[x,18,z],beam+"_y")

    # Rhythm of framed windows, sills, lintels and hinged shutters.
    for z,facing in ((8,"north"),(23,"south")):
        for x in (10,21):
            b.window(x,7,z,facing=facing)
    for z,facing in ((7,"north"),(24,"south")):
        for x in (9,15,21):
            b.window(x,14,z,facing=facing)
    for z in (10,20):
        b.window(25,14,z,facing="east")
    for z in (10,19):
        b.window(24,7,z,facing="east")

    # Actual two-part door, generous clear entry, warm suspended lights.
    f([16,5,8],[16,7,8],"air")
    p(16,5,8,"spruce_door_lower");p(16,6,8,"spruce_door_upper")
    p(16,7,8,"glass")
    f([14,9,7],[18,9,7],beam+"_x")
    for x in (14,18):
        p(x,8,7,"lantern_hanging")

    # A proper pitched, overhanging roof with a timber gable and ridge.
    for step in range(9):
        for z in (7,24):
            f([8+step,19+step,z],[24-step,19+step,z],wall)
    b.roof(6,26,5,26,19,roof)
    for z in (6,25):
        f([7,18,z],[25,18,z],beam+"_x")
        for step in range(10):
            for x in sorted({7+step,25-step}):
                p(x,19+step,z,beam+"_y")
        f([16,19,z],[16,28,z],beam+"_y")
        for x in (13,18):
            f([x,21,z],[x+1,23,z],"glass")
        f([12,20,z],[20,20,z],beam+"_x")
        f([12,24,z],[20,24,z],beam+"_x")

    # Secondary wing changes the silhouette and joins the main room internally.
    b.room([2,3,12],[7,9,22],wall)
    f([2,3,12],[7,4,22],"stone_bricks")
    f([3,4,13],[6,4,21],wood)
    for x in (2,7):
        for z in (12,22):
            f([x,5,z],[x,9,z],beam+"_y")
    b.window(4,6,12,facing="north")
    b.roof(1,7,11,23,10,roof,axis="z")
    f([8,5,15],[8,7,16],"air")
    for x in (1,7):
        f([x,9,12],[x,9,22],beam+"_z")

    # Structural stair access to the upper storey.
    for i,z in enumerate(range(12,20)):
        f([9,5+i,z],[10,5+i,z],"spruce_stairs_south")
    f([9,12,16],[10,12,18],"air")

    if "balcony" in features:
        f([10,12,4],[22,12,6],wood)
        for x in (10,22):
            f([x,5,4],[x,11,4],beam+"_y")
        for x in (10,13,19,22):
            p(x,13,4,"spruce_post")
        f([10,14,4],[22,14,4],"spruce_slab_bottom")
        for x in (10,22):
            f([x,14,4],[x,14,6],"spruce_slab_bottom")
        f([16,13,7],[16,14,7],"air")
        p(16,13,7,"spruce_door_lower");p(16,14,7,"spruce_door_upper")
        for x in (11,21):
            p(x,11,6,"lantern_hanging")
    else:
        for x in (11,21):
            f([x,5,5],[x,8,5],beam+"_y")
        f([11,9,5],[21,9,6],"spruce_slab_bottom")

    if "dormer" in features:
        # Side dormer interrupts the roof and gives the attic a framed window.
        b.room([21,23,11],[24,26,16],wall)
        f([22,24,12],[23,25,15],"air")
        f([24,24,13],[24,25,14],"glass")
        for z in (11,16):
            f([24,23,z],[24,26,z],beam+"_y")
        f([24,26,11],[24,26,16],beam+"_z")
        for step in range(2):
            f([24,27+step,12+step],[24,27+step,15-step],wall)
        b.roof(21,25,10,17,26,roof,axis="z")

    if "chimney" in features:
        f([21,14,19],[22,30,20],"bricks")
        for y in (17,23,29):
            f([21,y,19],[22,y,20],"stone_bricks")
        f([20,31,18],[23,31,21],"stone_brick_slab_bottom")

    if "interior" in features:
        for x in (15,21):
            p(x,5,17,"spruce_post")
            f([x-1,6,16],[x+1,6,18],"oak_slab_top")
            for z in (15,19):
                f([x-1,5,z],[x+1,5,z],
                  "spruce_stairs_south" if z==15 else "spruce_stairs_north")
        f([20,5,11],[22,5,13],"oak_planks")
        f([20,6,11],[22,6,13],"spruce_slab_top")
        f([14,5,10],[17,5,13],"red_carpet")
        for x,z in ((11,10),(22,20)):
            p(x,10,z,"lantern_hanging")
            p(x,11,z,"oak_planks")
        # Upper loft seating kept clear of the stairs and balcony door.
        f([20,13,19],[23,13,19],"spruce_stairs_north")
        f([20,13,21],[23,13,21],"oak_slab_bottom")
        f([7,18,20],[25,18,20],beam+"_x")
        p(21,17,20,"lantern_hanging")

    if "garden" in features:
        # Garden beds, flowering hedges, bench, and coherent small trees.
        for x0,x1,z0,z1 in ((2,7,8,9),(25,28,5,8),(25,28,11,13)):
            f([x0,3,z0],[x1,3,z1],"flowering_azalea")
        for x,z in ((8,3),(9,2),(21,2),(22,3),(26,15),(27,18),(5,10),(3,11)):
            p(x,3,z,"poppy" if rng.random()<.5 else "dandelion")
        f([24,3,3],[28,3,3],"spruce_slab_bottom")
        f([24,4,4],[28,4,4],"spruce_shutter_north")
        for cx,cz,h,radius in ((3,4,6,3),(28,25,5,2)):
            f([cx,3,cz],[cx,3+h,cz],"oak_log_y")
            for dy in range(-2,3):
                r=radius-(1 if abs(dy)==2 else 0)
                for dz in range(-r,r+1):
                    reach=max(0,int(math.sqrt(max(0,r*r-dz*dz))))
                    y=3+h+dy
                    f([cx-reach,y,cz+dz],[cx+reach,y,cz+dz],"oak_leaves")
            p(cx,3+h,cz,"oak_log_y")
        for x,z in ((12,2),(27,10),(27,19)):
            p(x,3,z,"spruce_post");p(x,4,z,"lantern")

    return b.spec
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

VERSION = "0.2.0"
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


def export_java_structure(volume, profile="java-26.3"):
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


def generate(build, edition="both", java_profile="java-26.3", max_size=32,
             pack_version=(1, 0, 0)):
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
    checks.append("paired_door_halves")
    counts = Counter(volume["palette"][i] for i in volume["cells"] if i >= 0)
    report = {
        "generator_version": VERSION, "schema": SCHEMA, "name": name,
        "edition": edition, "java_profile": java_profile if edition != "bedrock" else None,
        "bedrock_profile": "bedrock-1.26.30" if edition != "java" else None,
        "pack_version": list(pack_version), "size": volume["size"],
        "door_pairs": door_pairs,
        "placed_blocks": sum(counts.values()) - counts.get("air", 0),
        "explicit_air": counts.get("air", 0), "omitted_cells": volume["cells"].count(-1),
        "validation": {"level": "structural", "passed": True, "checks": checks,
                       "minecraft_tested": False},
        "sha256": {key: hashlib.sha256(value).hexdigest() for key, value in outputs.items()},
    }
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

Las posiciones omitidas conservan el mundo; el aire explicito vacia posiciones.
Para pruebas, usa un mundo creativo de ensayo con espacio libre y permisos.
Si actualizas el mismo pack Bedrock, incrementa --pack-version (ejemplo: 1.0.1).
Conserva el .build.json o .request.json para revisiones. preview.svg muestra una vista 3D.
preview_planos.svg contiene las tres proyecciones. revision.json incluye comprobaciones orientativas.
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

Kit v0.2.0. Fuente: https://github.com/Aldeanoo/aldeano-build-generator. Licencia MIT. Copyright (c) 2026 Aldeanoo.
SHA-256 de generator.py: 91dfac2bf75e919c0def794bdf5d9f5243726dae69cd80c0dde8ee7e693e2a1c
SHA-256 de architect.py: 2d5ad55691babc18e2976feffca8aed550caa61a47690936ddbcfc5524e0e5f1
Comienza ahora con las preguntas que falten; no des una explicacion larga del funcionamiento del kit.
