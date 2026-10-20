# Compatibilidad Técnica y Especificación NBT

Este documento detalla la compatibilidad de **Aldeano Build Generator** con las distintas ediciones de Minecraft, formatos de archivos de estructura y visores independientes.

---

## 🟩 Minecraft Bedrock Edition

- **Formato:** `.mcstructure` (NBT binario nativo, codificación Little-Endian, sin compresión GZIP).
- **Versión de formato:** `format_version: 1`.
- **Motor mínimo verificado:** Bedrock Engine `1.26.30+`. Compatible con versiones actuales de Minecraft Bedrock en Windows, Android, iOS, Xbox, PlayStation y Nintendo Switch.
- **Empaquetado (`.mcpack`):**
  - Paquete de comportamiento (*Behavior Pack*) estándar con `manifest.json`.
  - Estructuras almacenadas en la ruta interna `structures/<nombre>.mcstructure`.
  - UUIDs deterministas e independientes para cabecera y módulo de datos.
  - Soporte de incremento de versión con `--pack-version` para actualizaciones de mundos.

---

## ☕ Minecraft Java Edition

Aldeano Build Generator soporta de forma nativa los dos perfiles principales de Minecraft Java mediante el selector `--java-profile`:

### Perfil 1: `java-1.21.1` (Predeterminado)
- **DataVersion:** `3955` (Minecraft 1.21.1).
- **Formato NBT:** Big-Endian comprimido con GZIP estándar (RFC 1952).
- **Estructura de Paleta:** Lista de compuestos con claves canónicas `Name` (String con prefijo de namespace) y `Properties` (Compound con estados de bloque).
- **Datapack (`.datapack.zip`):**
  - `pack_format: 48` en `pack.mcmeta`.
  - Ruta de plantilla interna: `data/aldeano/structure/<nombre>.nbt`.
  - Invocación en juego: `/place template aldeano:<nombre> ~ ~ ~`.

### Perfil 2: `java-26.3` (Experimental / Snapshots futuras)
- **DataVersion:** `5023`.
- **Formato NBT:** Big-Endian comprimido con GZIP.
- **Estructura de Paleta:** Claves normalizadas `id` y `properties`.
- **Datapack:** Formato adaptativo con `min_format` y `max_format` `[121, 0]`.

---

## 🔬 Verificación Independiente y Visores NBT

Cada estructura generada se valida internamente y ha sido comprobada contra lectores independientes de la industria:

1. **`nbtlib` (Python):** Verificación de estructura de árbol NBT, tipos de etiquetas (`Byte`, `Int`, `List`, `Compound`, `String`) y cálculo de CRC32 GZIP.
2. **`prismarine-nbt` (JavaScript / Node.js):** Decodificación idéntica byte a byte de las estructuras Bedrock y Java.
3. **Visores Web de Terceros:**
   > [!IMPORTANT]
   > Muchos visores web comunitarios (como editores de esquemas no oficiales) solo aceptan el formato legado `.schematic` de WorldEdit o `.litematic` de Litematica.  
   > Los archivos generados por Aldeano Build Generator son **estructuras oficiales nativas de Mojang** (`.nbt` para `/place template` y `.mcstructure` para Bloque de Estructura). No intentes abrirlos en editores que no soporten estructuras vanilla de Mojang 1.21+.

---

## ⚙️ Dependencias y Entorno de Ejecución

- **Generación y Runtime:** Requiere **Python 3.10 o superior**. Cero librerías externas necesarias (usa únicamente módulos de la biblioteca estándar: `gzip`, `struct`, `hashlib`, `json`, `pathlib`, `re`, `zipfile`).
- **Pruebas de desarrollo:** La suite de 52 pruebas unitarias utiliza `unittest` estándar y, opcionalmente, `nbtlib` y `jsonschema` para comprobaciones de regresión profunda.
