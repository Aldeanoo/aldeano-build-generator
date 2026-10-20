# Importación en Minecraft Java Edition

> [!TIP]
> Esta guía ha sido ampliada y centralizada con instrucciones detalladas para Datapacks vanilla y Bloques de Estructura en:
> **👉 [Guía Universal de Importación](GUIA_DE_IMPORTACION.md#3-minecraft-java-edition)**

---

## Resumen Rápido

- **Datapack Vanilla (`.datapack.zip` - Recomendado):** Copia el archivo ZIP dentro de `datapacks/` en la carpeta de tu mundo, entra al juego (o escribe `/reload`) y ejecuta:
  ```text
  /place template aldeano:<nombre_construccion> ~ ~ ~
  ```
- **Bloque de Estructura (`.nbt`):** Copia el `.nbt` dentro de `generated/aldeano/structures/` en tu mundo, coloca un bloque de estructura en modo **Cargar** y escribe `aldeano:<nombre_construccion>`.

Para detalles técnicos sobre los perfiles `java-1.21.1` (DataVersion 3955) y `java-26.3` (DataVersion 5023), consulta [Compatibilidad](COMPATIBILIDAD.md).
