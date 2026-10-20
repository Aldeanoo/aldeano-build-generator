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
