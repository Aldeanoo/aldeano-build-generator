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
