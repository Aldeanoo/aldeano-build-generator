# Procedimiento de ejecución

Los bloques architect.py y generator.py incluyen componentes, compilador y perfiles.
No necesita pip, API keys ni dependencias externas para generar.

Si el TXT adjunto existe como archivo en tu entorno, extrae los bloques por programa:
busca cada encabezado real al PRINCIPIO de línea, toma su bloque
Python hasta la siguiente línea de cierre y guárdalo con ese nombre. Así no necesitas
volver a escribir todo el código en una respuesta. Detecta la ruta real automáticamente o usa la indicada.
Para extraerlos sin volver a emitir miles de tokens de código:

~~~python
import glob, re
from pathlib import Path
candidates = list(Path("/mnt/data").glob("*INICIO_IA*.txt")) + list(Path(".").glob("*INICIO_IA*.txt")) + list(Path(".").glob("*.txt"))
txt_path = candidates[0] if candidates else Path("INICIO_IA.txt")
kit = txt_path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
for name in ("architect.py", "generator.py"):
    pattern = r"(?ms)^## " + re.escape(name) + r" -[^\r\n]*\r?\n+```python\r?\n(.*?)^```[ \t\r]*$"
    match = re.search(pattern, kit)
    if match is None:
        raise ValueError("Falta el bloque completo de " + name)
    Path(name).write_text(match.group(1).rstrip() + "\n", encoding="utf-8")
~~~

Si solo puedes acceder por red desde Python, descarga los dos archivos de la misma
release del repositorio. Sin archivo ni red, conserva el diseño y pide el TXT completo.

1. Escribe los dos bloques como architect.py y generator.py en la misma carpeta.
2. Escribe la solicitud de arquitectura o BuildSpec como design.build.json.
3. Ejecuta con Python 3.10 o posterior:

~~~text
python generator.py design.build.json --edition both --java-profile java-1.21.1 --output work
~~~

Usa --edition bedrock o --edition java si solo se necesita una.
Elige el perfil declarado: --java-profile java-1.21.1 o java-26.3.
La CLI exige perfil explícito para Java; nunca presupone 26.3.
No cambies solo DataVersion ni renombres .mcstructure a .nbt para convertir.
Hasta 48 bloques por eje: --max-size 48 solo si hace falta.
Para revisiones utiliza otra carpeta de salida.
Si mantienes el nombre del pack Bedrock, aumenta --pack-version 1.0.1.

4. Lee work/validacion.json y work/revision.json. Revisa work/preview.svg si tu entorno lo permite (no transcribas el texto SVG crudo en el chat para no exceder los límites de tokens).
5. Si falla el diseño, corrígelo y vuelve a ejecutar.
6. Prepara la entrega elegida en otra carpeta, conservando work solo internamente:

~~~text
python generator.py design.build.json --delivery mcstructure --output entrega
python generator.py design.build.json --delivery nbt --java-profile java-1.21.1 --output entrega
python generator.py design.build.json --delivery structures --java-profile java-1.21.1 --output entrega
~~~

Son alternativas: ejecuta solo la elegida, con el perfil y opciones de la revisión.
mcstructure produce un único .mcstructure; nbt, un único .nbt;
structures, solo esos dos archivos. No añade ZIP, JSON ni previews.
Para el paquete completo, usa work (--delivery full, predeterminado).
La escritura se hace en binario, con lectura de comprobación, CRC y reemplazo atómico
por archivo. Si falla, no entregues ese archivo ni anuncies éxito.

7. Verifica los binarios guardados, usando sus rutas reales:

~~~text
python generator.py --verify entrega/nombre.nbt --java-profile java-1.21.1
python generator.py --verify entrega/nombre.mcstructure
~~~

Solo ejecuta las verificaciones pertinentes. Lee ok, verification.passed y sha256.
El verificador es estricto para archivos de este generador; no es un importador NBT universal.
Adjunta ÚNICAMENTE los archivos solicitados que existan y hayan pasado la verificación.
Paquete completo por edición:

- Bedrock Windows: nombre.mcstructure y nombre.mcpack.
- Bedrock móvil: nombre.mcpack; apertura pendiente de probar por sistema.
- Java: nombre.nbt y nombre.datapack.zip.
- Ambos: enlaces separados; el ZIP general es opcional.
- Revisiones: conserva nombre.request.json si existe y nombre.build.json.

8. Lee work/LEEME.txt para proporcionar los pasos mínimos, si los necesita.

El generador comprueba formato y geometría; no abre Minecraft.
No declares una prueba dentro del juego que no has realizado.
No intentes modificar desde el chat las carpetas del mundo del usuario.

Si la plataforma bloquea la extensión solicitada, explica la limitación y ofrece
un ZIP que contenga SOLO ese archivo, sin disfrazar texto como binario.
Sin creación de archivos, devuelve el JSON como texto y comunica la limitación.

Uso de los archivos:

- .mcstructure: importar con bloque de estructura en Bedrock Windows.
- .mcpack: importar, activar behavior pack y /structure load.
- .datapack.zip: copiar en datapacks/ del mundo Java, /reload y /place template.
- .nbt: copiar a generated/aldeano/structures/nombre.nbt dentro del mundo Java;
  bloque de estructura en Cargar, nombre aldeano:nombre. No abrir por doble clic.
  Un visor debe soportar GZIP, NBT big-endian y la paleta del perfil elegido.
- .build.json: diseño reutilizable, no se importa directamente a Minecraft.
- .request.json: solicitud compacta para cambiar tema y detalles.
- preview.svg: vista 3D final; preview_planos.svg: tres proyecciones.
- revision.json: diagnósticos orientativos, sin puntuación estética.
