# Aldeano Build Generator

**Pega el kit en una IA, responde unas preguntas y genera una construcción detallada para Minecraft.**

Versión **v0.2.1** · Python estándar · Bedrock y Java · Cero dependencias externas · Sin API keys.

> [!NOTE]
> Los archivos binarios (`.mcstructure`, `.nbt`, `.datapack.zip`) pasan verificaciones técnicas rigurosas y se contrastan con lectores NBT independientes (`nbtlib` y `prismarine-nbt`).

---

## 🚀 Probar con una IA (Inicio Rápido)

### Opción 1: Copiar el Master Prompt en cualquier IA (Recomendado)
Abre **[MASTER_PROMPT.md](MASTER_PROMPT.md)** o copia el siguiente mensaje y pégalo directamente en tu IA favorita (**ChatGPT Free / Plus, Claude Free / Pro, Gemini, DeepSeek, Copilot**):

~~~text
Actúa como Maestro Arquitecto de Minecraft de "Aldeano Build Generator".
Quiero que me ayudes a diseñar y construir lo que te pida (castillos, templos, fortalezas, casas, torres, barcos o cualquier edificio) con máxima calidad estética, profundidad y detalle (nada de cubos planos ni cajas huecas).
Pregúntame qué quiero construir si no te lo he indicado todavía, o empieza directamente a diseñar mi idea si ya te la he descrito.
Aplica reglas de volumetría dinámica, zócalos de piedra, pilares estructurales salientes, tejados con aleros de 1 bloque y puertas dobles.
Si tienes ejecución de Python en tu entorno, compila y entrega los archivos descargables (.mcstructure, .nbt, .datapack.zip).
Si no tienes ejecución de código, entrega el diseño JSON aldeano-build/v1, la lista de materiales en stacks y el plano por capas para supervivencia.
~~~

> [!TIP]
> **¿Qué IA estás usando?**  
> - **En IAs con Python (ChatGPT Plus / Team / Pro con Code Interpreter):** Descarga **[INICIO_IA.txt](https://raw.githubusercontent.com/Aldeanoo/aldeano-build-generator/v0.2.1/INICIO_IA.txt)** y adjúntalo en la conversación para que la IA genere los archivos binarios directamente descargables.
> - **En IAs gratuitas (ChatGPT Free, Claude Free, Gemini, DeepSeek):** La IA diseñará la estructura en JSON y podrás compilarla en tu ordenador en 0.1 segundos con un solo comando.  
> 👉 Consulta la **[Guía de Uso: IA Free vs IA de Pago](docs/GUIA_IA_FREE_VS_PRO.md)**.

---

## 🏰 Construcciones Destacadas (Descarga Directa)

Puedes probar de inmediato las estructuras ya generadas y verificadas:

![Posada del Roble](samples/posada_del_roble/preview_3d.png)

- **[Descargar Posada del Roble completa (.todo.zip)](https://github.com/Aldeanoo/aldeano-build-generator/releases/download/v0.2.1/posada_del_roble.todo.zip)**
- Descargas sueltas: [Bedrock .mcstructure](https://github.com/Aldeanoo/aldeano-build-generator/releases/download/v0.2.1/posada_del_roble.mcstructure) · [Java 1.21.1 .nbt](https://github.com/Aldeanoo/aldeano-build-generator/releases/download/v0.2.1/posada_del_roble.nbt)

| Construcción | Tamaño (X × Y × Z) | Vista Previa | Paquete Completo |
| :--- | :---: | :---: | :--- |
| **Posada del Roble** | 31 × 32 × 29 | [Ver SVG](samples/posada_del_roble/preview.svg) | [Descargar ZIP](https://github.com/Aldeanoo/aldeano-build-generator/releases/download/v0.2.1/posada_del_roble.todo.zip) |
| **Casa Medieval** | 19 × 19 × 17 | [Ver SVG](samples/casa_medieval/preview.svg) | [Descargar ZIP](https://github.com/Aldeanoo/aldeano-build-generator/releases/download/v0.2.1/casa_medieval.todo.zip) |
| **Torre de Vigía** | 13 × 24 × 13 | [Ver SVG](samples/torre_vigia/preview.svg) | [Descargar ZIP](https://github.com/Aldeanoo/aldeano-build-generator/releases/download/v0.2.1/torre_vigia.todo.zip) |
| **Puente Rústico** | 23 × 9 × 11 | [Ver SVG](samples/puente_rustico/preview.svg) | [Descargar ZIP](https://github.com/Aldeanoo/aldeano-build-generator/releases/download/v0.2.1/puente_rustico.todo.zip) |

Cada paquete ZIP incluye las estructuras binarias para ambas ediciones, los packs de comportamiento/datapacks listos para instalar, el diseño reutilizable JSON, lista de materiales y guía de colocación. También puedes explorar los archivos individuales en [samples/](samples/).

---

## 🎮 ¿Cómo colocar la construcción en tu mundo?

> 👉 **[Guía Universal de Importación Paso a Paso](docs/GUIA_DE_IMPORTACION.md)** (Windows, Móvil Android/iOS, Consolas y Java Edition).

### Resumen Rápido:
- **Bedrock Windows (`.mcstructure`):** En el juego, obtén un bloque de estructura con `/give @s structure_block`, cambia el modo a **Cargar**, pulsa **Importar**, selecciona tu `.mcstructure` y pulsa **Cargar**.
- **Bedrock Móvil y PC (`.mcpack`):** Abre el archivo `.mcpack` con Minecraft, activa el paquete de comportamiento en los ajustes de tu mundo y ejecuta en el chat:
  ```text
  /structure load aldeano:<nombre_construccion> ~ ~ ~
  ```
- **Java Edition (`.datapack.zip` - Recomendado):** Copia el archivo ZIP dentro de la subcarpeta `datapacks/` de tu mundo, entra al juego (o ejecuta `/reload`) y ejecuta:
  ```text
  /place template aldeano:<nombre_construccion> ~ ~ ~
  ```
- **Java Edition (`.nbt`):** Copia el archivo en `generated/aldeano/structures/` dentro de tu mundo y cárgalo con un bloque de estructura vanilla (`aldeano:<nombre_construccion>`).

---

## 💻 Generación Local (Línea de Comandos)

Requiere **Python 3.10 o posterior** en tu sistema. No necesita instalar dependencias externas (`pip`):

```bash
# Generar para ambas ediciones con perfil Java 1.21.1:
python generator.py examples/posada.request.json --edition both --java-profile java-1.21.1 --output output

# Generar solo los dos binarios (.mcstructure y .nbt):
python generator.py examples/posada.request.json --delivery structures --java-profile java-1.21.1 --output output

# Verificar la integridad técnica de una estructura guardada:
python generator.py --verify output/posada_del_roble.nbt --java-profile java-1.21.1
python generator.py --verify output/posada_del_roble.mcstructure
```

### Opciones CLI principales:
- `--edition bedrock | java | both`: Edición de Minecraft de destino.
- `--java-profile java-1.21.1 | java-26.3`: Perfil de DataVersion para Java.
- `--delivery mcstructure | nbt | structures | full`: Entrega mínima de binarios o paquete completo.
- `--max-size 32 | 48`: Límite máximo de bloques por eje (32 por defecto, ampliable a 48).
- `--catalog`: Imprime en formato JSON el catálogo canónico de materiales y perfiles soportados.

---

## 📦 Especificaciones del Generador

- **Bedrock:** `.mcstructure` v1 Little-Endian nativo y paquetes `.mcpack` con manifiesto UUID.
- **Java:** `.nbt` Big-Endian comprimido con GZIP (RFC 1952) y datapacks listos para `/place template`.
- **Catálogo Canónico:** Exactamente 82 materiales seleccionados con soporte de estados direccionales (`axis`, `facing`, `half`, `open`).
- **Verificación Estricta:** Detección de fallos de CRC GZIP, truncamiento, etiquetas erróneas y puertas desparejadas antes de la exportación.
- **Esquemas Formales:** [Esquema JSON Build](schema/aldeano-build-v1.schema.json) · [Catálogo](catalog/canonical.json).

---

## 🧪 Pruebas Automatizadas y Calidad de Código

El repositorio cuenta con **52 pruebas unitarias automatizadas** que cubren validaciones de límites, coordenadas asimétricas, omisión vs aire explícito, ambas versiones Java, empaquetado, reproducibilidad byte a byte y ejecución aislada (`python -S`):

```bash
# Instalar herramientas de desarrollo opcionales:
python -m pip install -r requirements-dev.txt

# Ejecutar la suite completa de 52 pruebas:
python -m unittest discover -s tests -v

# Verificar la integridad del bundle de IA:
python tools/build_ai_bundle.py --check
```

---

## 📚 Documentación Centralizada

- **[MASTER_PROMPT.md](MASTER_PROMPT.md):** El mensaje inicial definitivo para copiar y pegar en cualquier IA.
- **[Guía Universal de Importación](docs/GUIA_DE_IMPORTACION.md):** Instrucciones detalladas para Bedrock (PC/Móvil/Consolas) y Java.
- **[Guía IA Free vs de Pago](docs/GUIA_IA_FREE_VS_PRO.md):** Cómo aprovechar el generador según tu nivel de IA.
- **[Compatibilidad Técnica y NBT](docs/COMPATIBILIDAD.md):** Especificación técnica de perfiles Java 1.21.1 vs 26.3 y lectores NBT.
- **[Documentación Interna y Metodología](docs/internals/):** Arquitectura procedural, papers académicos y resultados históricos de pruebas.

---

## Licencia y Créditos

Distribuido bajo la **Licencia MIT**. Consulta [LICENSE](LICENSE) y [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) para más detalles.  
Proyecto independiente de código abierto, no afiliado con Mojang Studios ni Microsoft.
