# Compatibilidad técnica

Estado: experimental. Validación estructural significa comprobar NBT, paletas,
coordenadas y packs. No significa haber colocado el archivo en Minecraft.

| Salida | Datos | Verificación técnica | En el juego |
| --- | --- | --- | --- |
| Bedrock v1 | 1.26.30 | Dos capas, orden Z rápido, paleta 18168865 | Pendiente |
| mcpack | Motor mínimo 1.26.30 | Manifiesto, UUID y rutas | Pendiente |
| Java 26.3 | DataVersion 5023, pack 121.0 | id, GZIP y rutas | Pendiente |
| Java 1.21.1 | DataVersion 3955, pack 48 | Name, GZIP y rutas | Pendiente |

37 entradas: 36 materiales de construcción y air. Identificadores y estados
contrastados con los datasets siguientes. Cuarzo usa pillar_axis=y en Bedrock.

## Procedencia

- [PrismarineJS, commit 201ca802](https://github.com/PrismarineJS/minecraft-data/tree/201ca802a1b2c968b02e7fa5b31dd74e8bff3d8b/data/bedrock/1.26.30).
- [Versiones Java, commit 04465b70](https://github.com/misode/mcmeta/tree/04465b70129d4a47da0526643a88f69e59c34778).
- Se inspeccionó una paleta vanilla 26.3, sin redistribuir la construcción:
  [plains_small_house_1.nbt](https://github.com/misode/mcmeta/blob/26.3-data/data/minecraft/structure/village/plains/houses/plains_small_house_1.nbt).
- [Manifiesto oficial Mojang](https://piston-meta.mojang.com/mc/game/version_manifest_v2.json).
- [Formato Bedrock en Amulet](https://github.com/Amulet-Team/Amulet-Core/blob/1.9.46/amulet/level/formats/mcstructure/format_wrapper.py).

Los fixtures geométricos y ejemplos son propios.
Para verificar en el juego: versión, SO, hash, método, origen, ejes y aire/omisión.
Actualizar el estado solo tras esa prueba.

Las 45 entradas detalladas se contrastan con `python tools/update_detail_catalog.py`.
Se comprueban los tipos Byte/Int/String de Bedrock y Properties/properties de Java.
Las formas de la preview son esquem?ticas; la navegaci?n se debe probar en el juego.
