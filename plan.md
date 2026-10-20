# Aldeano Build Generator — Plan de repositorio para usar con IA

Fecha de investigación y revisión: 20 de octubre de 2026.
Estado: plan de referencia. Ya existe un prototipo v0.1.0 del generador, las instrucciones y las pruebas automatizadas. El alcance real y los resultados están en README.md y docs/test-results.md. Siguen pendientes las pruebas en cuentas gratuitas y dentro de Minecraft.

## 1. Objetivo y decisión recomendada

Crear un repositorio público que el suscriptor presente a ChatGPT Free o Claude Free para que la IA lea unas instrucciones, haga pocas preguntas, diseñe la construcción y entregue el archivo descargable.

**El producto principal es un kit de instrucciones conversacionales con un generador ya escrito y probado que la IA puede ejecutar.** El suscriptor no programa, no instala el repositorio ni configura una API key.

Flujo objetivo: **pegar enlace/instrucciones → responder → descargar**. Una web de conversión queda como alternativa para conversaciones sin ejecución; deja de ser un paso obligatorio.

La IA se encarga del diseño. El compilador incluido escribe los archivos. Así se evita pedir al modelo que reinvente en cada conversación la lógica de un formato binario.

La extensión correcta es `.mcstructure` y corresponde a Bedrock. Para Java se generará una estructura `.nbt` y un datapack. Un mismo diseño puede producir ambas salidas, pero un único archivo no se presenta como nativo de las dos ediciones. [Plantillas por edición](https://learn.microsoft.com/en-us/minecraft/creator/documents/structures/introductiontojigsawstructures?view=minecraft-bedrock-stable).

Supuesto inicial: los suscriptores son la comunidad destinataria; comprobar una suscripción de pago no forma parte del lanzamiento. Un repositorio público puede compartirse.

## 2. Viabilidad en ChatGPT Free y Claude Free

Separar tres capacidades: leer instrucciones, producir un diseño de texto y ejecutar código para adjuntar un archivo binario real.

| Capacidad | Tratamiento |
| --- | --- |
| Seguir instrucciones pegadas y hacer preguntas | Contrato conversacional básico que se evaluará |
| Leer un enlace de GitHub | Ruta cómoda cuando la sesión puede acceder al contenido |
| Leer automáticamente todos los archivos del repositorio | No se presupone: proporcionar entrada autosuficiente |
| Ejecutar Python y adjuntar resultados | Ruta principal cuando están disponibles esas herramientas |
| Generar solo texto | Conservar el diseño y ofrecer una ruta adicional de conversión |

**Claude Free:** Anthropic documenta ejecución de código y creación de archivos para usuarios gratuitos. Esto justifica probar el flujo dentro de Claude, pero todavía hay que verificar nuestro generador y la descarga de sus formatos concretos. Las cuotas siguen aplicando. [Crear y editar archivos con Claude](https://support.claude.com/es/articles/12111783-crear-y-editar-archivos-con-claude), [planes de Claude](https://support.claude.com/en/articles/11049762-choose-a-claude-plan).

**ChatGPT Free:** la documentación oficial consultada describe creación y descarga de archivos en ChatGPT, pero no establece que toda sesión gratuita pueda ejecutar este generador y adjuntar sus resultados. Antes de marcar ese flujo como verificado, probarlo con una cuenta Free real y registrar su superficie y herramientas. No deducir capacidades del chat a partir de la API o de Codex. [Documentación oficial de OpenAI sobre archivos](https://learn.chatgpt.com/docs/artifacts-viewer).

Las instrucciones no activan herramientas que la cuenta no tenga. Pegar una URL tampoco instala el repositorio ni garantiza su lectura completa.

Se publicarán dos matrices independientes: proveedor/sesión capaz de generar el archivo y edición/versión de Minecraft capaz de cargarlo.

## 3. Entrada del usuario y preguntas de la IA

### Ruta A: enlace

El README ofrecerá este mensaje para copiar, sustituyendo la URL al publicar:

~~~text
Quiero crear una construcción de Minecraft con este repositorio:
<URL_DEL_REPOSITORIO>

Lee INICIO_IA.md y sigue su flujo de preguntas.
Usa el generador incluido para crear el archivo descargable.
Si no puedes leer los recursos o ejecutar el generador, dímelo claramente.
~~~

Preferir enlaces a una release concreta. La IA debe obtener las instrucciones y los recursos necesarios, no limitarse a leer el título del README.

### Ruta B: archivo autosuficiente

Si no puede leer el enlace, copiar el contenido de `INICIO_IA.md` o adjuntar `INICIO_IA.txt` cuando la sesión permita adjuntos. Ambos contendrán el mismo kit: instrucciones, esquema reducido, catálogo, ejemplo y compilador en texto.

El suscriptor no deberá copiar cinco archivos ni reconstruir el código. La distribución básica tiene que funcionar sin acceso remoto a GitHub después de recibir el paquete.

### Preguntas: máximo cuatro, en un único mensaje

| Pregunta | Ejemplo | Valor si el usuario delega |
| --- | --- | --- |
| ¿Qué quieres construir y con qué estilo? | Casa medieval, puente japonés | Casa medieval sencilla |
| ¿Bedrock, Java o ambos? ¿Dispositivo y versión, si la sabes? | Bedrock en Windows | Ambos; perfiles predeterminados, indicando sus versiones |
| ¿Pequeño, mediano o medidas concretas? | 24 × 16 × 20 | Mediano, hasta 32 bloques por eje |
| ¿Qué detalles o interiores quieres? | Dos plantas, balcón | Entrada e interior utilizables |

Omitir preguntas ya respondidas. Aceptar «decide tú» y continuar con los valores predeterminados. No preguntar por NBT, coordenadas, paletas o dependencias.

Primera respuesta prevista:

~~~text
Vamos a preparar tu construcción. Respóndeme lo que sepas; puedes decir
«decide tú» para que elija los detalles:

1. ¿Qué quieres construir y con qué estilo?
2. ¿Bedrock, Java o ambos? ¿PC, móvil o consola? ¿Versión, si la sabes?
3. ¿Pequeño, mediano o unas medidas concretas?
4. ¿Qué detalles o interiores quieres incluir?
~~~

Tras las respuestas, describir brevemente la elección y generar sin otra aprobación. Si un requisito es incompatible, explicar la alternativa antes de cambiarlo. Conservar las preferencias para revisiones posteriores.

### Entrega según plataforma

- Bedrock Windows: `.mcstructure` directo y opción `.mcpack`.
- Bedrock móvil: priorizar `.mcpack`, con apertura/importación probada en el sistema.
- Java escritorio: datapack ZIP y `.nbt` como alternativa avanzada.
- Ambos: dos descargas desde el mismo diseño.
- Consolas: indicar la ruta adicional necesaria; no prometer importación directa.

Microsoft limita a Windows el botón de importar `.mcstructure` y requiere ser anfitrión. El tutorial móvil no debe depender de ese botón. [Importación en Bedrock](https://learn.microsoft.com/en-us/minecraft/creator/documents/structures/introductiontostructureblocks?view=minecraft-bedrock-stable).

Son tres etapas de generación: iniciar, responder y descargar. Instalar el contenido en Minecraft es un paso posterior.

## 4. Instrucciones del kit y contrato de ejecución

### INICIO_IA.md

Debe contener, en este orden:

1. Objetivo de la tarea y preguntas iniciales.
2. Valores predeterminados y límites.
3. Esquema BuildSpec y ejemplo completo.
4. Catálogo mínimo de los perfiles predeterminados.
5. Código literal del compilador y recursos necesarios.
6. Procedimiento de ejecución, validación y entrega.
7. Recuperación si faltan herramientas.
8. Versión y procedencia del kit.

Fragmento de instrucciones previsto:

~~~text
Ayuda al usuario a crear una construcción descargable de Minecraft.

Pregunta en un solo mensaje únicamente los datos que falten:
construcción/estilo, edición/dispositivo/versión, tamaño y detalles.

Si responde «decide tú», utiliza los valores predeterminados.
Cuando haya información suficiente, diseña y genera sin pedir otra confirmación.

Usa exclusivamente el esquema y catálogo incluidos.
Ejecuta el compilador incluido sin reescribir su lógica de formatos.
Si falla la validación, corrige el diseño y vuelve a ejecutar.

Entrega archivos descargables reales y los pasos de importación.
No inventes enlaces, ejecuciones ni pruebas dentro de Minecraft.

Si no puedes leer los archivos, solicita la entrada autosuficiente.
Si no puedes ejecutar código, conserva las respuestas y entrega el diseño
completo, explicando la alternativa disponible.
~~~

El texto actúa como manual de tarea que el usuario pide seguir. No debe afirmar que tiene prioridad sobre las reglas de la plataforma.

No basta con publicar `AGENTS.md` o `CLAUDE.md` y suponer que un chat normal los aplica. Si se añaden para herramientas de desarrollo, serán adaptadores secundarios; la entrada general será `INICIO_IA.md`.

### Paquete autosuficiente

- Generar Markdown y texto desde las mismas fuentes con `tools/build_ai_bundle.py`.
- Incluir solo los perfiles predeterminados y un ejemplo pequeño.
- Código legible; no obligar a reconstruir el compilador desde base64.
- Objetivo inicial: menos de 10.000 tokens estimados, sujeto a medición en las cuentas objetivo.
- No incluir este plan, todos los fixtures ni el historial del repositorio.
- Comprobar en CI que el compilador y catálogo del paquete coinciden con la release.
- Una vez recibido, compilar sin descargas de red ni instalación de dependencias.

### Comportamiento de ejecución

La IA escribe el JSON del diseño, ejecuta el compilador, lee el informe y corrige errores de datos antes de entregar.

CLI prevista:

~~~text
python generator.py design.build.json --edition both --output output
~~~

Usar los nombres reales y rutas del entorno. No inventar que el suscriptor tiene una carpeta local accesible desde el chat.

No presentar como descarga un bloque de código o una ruta que no exista. No afirmar que se ha probado cada construcción en Minecraft: la carga real se verifica para los perfiles del generador durante el desarrollo.

## 5. Arquitectura y alcance del MVP

~~~mermaid
flowchart TD
    A[Enlace o instrucciones completas] --> B[IA pregunta al suscriptor]
    B --> C[Preferencias y diseño JSON]
    C --> D[Compilador Python del repositorio]
    D --> E[Validación y volumen canónico]
    E --> F[Adaptador Bedrock]
    E --> G[Adaptador Java]
    F --> H[mcstructure y mcpack]
    G --> I[nbt y datapack zip]
    H --> J[Descargas en la conversación]
    I --> J
    C --> K[Alternativa si falta ejecución]
~~~

| Componente | Elección | Motivo |
| --- | --- | --- |
| Generador | Python 3 en un archivo | Portátil e incluible en texto |
| Dependencias de ejecución | Biblioteca estándar | No exigir paquetes ni conexión de red |
| NBT | Escritor limitado con `struct` | Tipos necesarios, con pruebas independientes |
| Compresión | `gzip` y `zipfile` | Archivos Java y packs |
| Diseño | `json` | Contrato pequeño y reutilizable |
| Pruebas | `unittest` y lector NBT independiente de desarrollo | Evitar validar solo contra nuestro propio escritor |
| Distribución | GitHub y releases | Kit, perfiles y ejemplos versionados |

El escritor NBT propio exige pruebas estrictas; no se presupone que el formato sea trivial. Prismarine NBT sirve como referencia independiente de formatos big-endian y little-endian. [Prismarine NBT](https://github.com/PrismarineJS/prismarine-nbt).

Funciones separadas para parsear, validar, expandir geometría, resolver paleta y exportar. Nunca ejecutar código contenido en la descripción: interpretar solo operaciones de datos validadas.

### Incluido

- Preguntas agrupadas y valores predeterminados.
- `set` y `fill`.
- Entre 24 y 40 materiales/estados canónicos verificados.
- Preset hasta 32³ y ampliación hasta 48³ después de probarla.
- Bedrock `.mcstructure` v1 y `.mcpack`.
- Java NBT y datapack ZIP.
- JSON reutilizable, materiales e informe de validación.
- Refugio, torre y puente como ejemplos.
- Preview esquemática opcional que no impida generar el archivo.

Estos límites de tamaño son del producto, no el límite universal de los formatos.

### Aplazado

Entidades, inventarios, carteles, NBT arbitrario, command blocks, redstone funcional, agua/anegamiento, mods y bloques personalizados. Añadir puertas, camas y escaleras tras verificar sus estados.

No son requisitos iniciales una web, un backend, API central, MCP, autenticación, galería ni entrenar un modelo.

Una casa del MVP puede tener entrada abierta y techo escalonado de bloques completos. Los ejemplos deben mostrar ese acabado.

## 6. Contrato de diseño para la IA: BuildSpec v1

Nombre de archivo: `nombre.build.json`.
Identificador de esquema: `aldeano-build/v1`.
Coordenadas locales: `[x, y, z]`; Y es altura; origen en la esquina inferior del volumen.
Operaciones en orden; la última escritura sobre una celda gana.

La IA usa identificadores canónicos como `oak_planks`. No escribe IDs numéricos, estados internos de Bedrock, DataVersion, rutas o NBT.

### Ejemplo completo

Este ejemplo produce un pequeño refugio con suelo, paredes, interior vacío, acceso y techo plano. Usa un volumen de 9 × 6 × 9.

~~~json
{
  "schema": "aldeano-build/v1",
  "name": "refugio_roble",
  "size": [9, 6, 9],
  "palette": {
    "floor": "stone_bricks",
    "wall": "oak_planks",
    "roof": "spruce_planks",
    "empty": "air"
  },
  "ops": [
    {"op": "fill", "from": [0, 0, 0], "to": [8, 0, 8], "block": "floor"},
    {"op": "fill", "from": [0, 1, 0], "to": [8, 4, 8], "block": "wall"},
    {"op": "fill", "from": [1, 1, 1], "to": [7, 4, 7], "block": "empty"},
    {"op": "fill", "from": [4, 1, 0], "to": [4, 2, 0], "block": "empty"},
    {"op": "fill", "from": [0, 5, 0], "to": [8, 5, 8], "block": "roof"}
  ]
}
~~~

### Semántica obligatoria

| Campo/operación | Regla |
| --- | --- |
| `schema` | Valor exacto `aldeano-build/v1` |
| `name` | De 1 a 48 caracteres; minúsculas, números y guion bajo |
| `size` | Tres enteros positivos, dentro del límite activo |
| `palette` | Entre 1 y 64 alias; valores del catálogo canónico |
| `ops` | Entre 1 y 512 operaciones; objetivo recomendado para la IA: 80 o menos |
| `set` | `{"op":"set","at":[x,y,z],"block":"alias"}` |
| `fill` | Cuboide con ambos extremos incluidos; `from` no supera `to` en ningún eje |
| Alias | Formato restringido y sin claves reservadas; todas las referencias deben existir |
| Coordenadas | Enteros entre cero y `size[eje] - 1` |
| Campos extra | Rechazados; no ejecutar extensiones o código incrustado |

Para interiores hay que distinguir:

- **Celda sin escribir:** no modificar el bloque existente del mundo.
- **`air` explícito:** colocar aire y vaciar esa posición.

El volumen comienza con celdas sin escribir. Al exportar Bedrock se representan con el valor de omisión del formato; en Java se omiten de la lista de bloques. Un `fill` de aire sigue siendo una escritura explícita. Esto evita que los huecos de una construcción se rellenen con terreno existente.

### Límites de entrada y expansión

- JSON de hasta 256 KiB; comprobar el tamaño antes de parsear.
- Preset normal: 32³ = 32.768 posiciones.
- Tope ampliado planificado: 48³ = 110.592 posiciones.
- Máximo de 4.000.000 de escrituras estimadas acumuladas por diseño.
- Presupuesto calculado antes de expandir: sumar el volumen de cada `fill` y los `set`.
- Límites de profundidad y longitud de textos; no permitir operaciones anidadas.
- Contenedores de alias sin prototipo o Map; rechazar `__proto__`, `constructor` y `prototype`.
- Rechazar rutas, URLs, NBT arbitrario y cualquier operación fuera del contrato.

No basta con limitar el volumen final: cientos de operaciones superpuestas también pueden consumir demasiado trabajo.

### Evolución posterior

Añadir `line`, `roof` o `repeat` solo si las pruebas de generación muestran que reducen errores y longitud. Es preferible mantener dos operaciones bien definidas antes que una gramática extensa que las IA gratuitas interpreten de manera desigual.

## 7. Compatibilidad y catálogo de bloques

### Política de versiones

La promesa será: «compatible con las versiones que aparecen como verificadas», no «compatible con todas las versiones de Minecraft».

En la fecha de investigación hay documentación oficial de Java 26.3 y de la familia Bedrock 26.50 con hotfixes posteriores. Las notas de Java y Bedrock muestran cambios de formato relevantes. La versión exacta instalada para las pruebas se registrará antes de congelar cada perfil. [Versiones publicadas](https://feedback.minecraft.net/hc/en-us/sections/360001186971-Release-Changelogs), [Java 26.3](https://feedback.minecraft.net/hc/en-us/articles/48913133328013-Minecraft-Java-Edition-26-3).

Perfiles previstos:

| Perfil | Objetivo | Condición para publicarlo |
| --- | --- | --- |
| Bedrock actual | Familia 26.50, con hotfix exacto registrado | Fixture y carga real por ambas rutas de Windows |
| Java actual | 26.3 | Fixture propio, datapack reconocido y colocación real |
| Bedrock anterior | Una versión anterior accesible para prueba | Catálogo y prueba independientes |
| Java anterior | Una versión concreta de la serie 1.21 | Adaptador y pack correspondientes a esa versión |

Los dos perfiles actuales son obligatorios para v1.0. Los anteriores se incorporan después; no deben retrasar una primera versión compatible con ambas ediciones actuales.

Cada perfil debe contener:

- ID interno y nombre exacto de la versión.
- Procedencia y fecha de los fixtures.
- Revisión del catálogo canónico.
- Mapeos de materiales y estados.
- Versión de datos de Java o de paleta de Bedrock, según corresponda.
- Forma del NBT, metadatos del pack y ruta interna de estructuras.
- Estado: `experimental`, `verificado` o `retirado`.
- Referencia a la prueba dentro del juego y sus resultados.

No confundir el DataVersion de Java, la versión del datapack, el `format_version` de `.mcstructure` y la versión de bloque de la paleta Bedrock: son valores distintos.

### Mapeo canónico

Formato conceptual:

~~~text
material canónico
  → Java: identificador + propiedades verificadas para ese perfil
  → Bedrock: identificador + estados NBT tipados + versión de paleta
  → color de preview + nombre en español
~~~

La IA solo recibe materiales que tengan ambos mapeos cuando se solicite compatibilidad dual. No asumir que compartir nombre implica compartir estados. Los datos de PrismarineJS pueden ayudar a comprobar identificadores y estados, pero no proporcionan por sí solos un conversor universal ni sustituyen las pruebas. [Datos Bedrock de PrismarineJS](https://github.com/PrismarineJS/minecraft-data/blob/master/doc/bedrock.md).

Empezar por bloques completos estables: piedra, adoquín, tablones, ladrillos, cristal y una selección de terracota o lana. La lista exacta se congela con fixtures. Añadir troncos por eje y losas únicamente tras verificar los estados de cada edición.

Un material desconocido bloquea la exportación. Si una preferencia exige otra opción, explicar la alternativa; las elecciones delegadas utilizan el catálogo disponible.

## 8. Exportación Bedrock

### Archivo `.mcstructure`

Implementar primero **v1**, que sigue cargando en Bedrock 26.50 según Mojang. La misma nota introduce v2: índices en IntArray y segunda capa opcional cuando está vacía. Esto permite elegir v1 por compatibilidad inicial y dejar la optimización v2 para después. [Fuente oficial: cambios de estructuras en Bedrock 26.50](https://www.minecraft.net/tr-tr/article/minecraft--bedrock-edition-26-50-changelog).

El contenedor es NBT little-endian sin compresión. La estructura incluye tamaño, origen, índices, paleta y entidades; el código de Amulet permite contrastar los tipos y el recorrido. Para v1, ambas listas de índices deben cubrir el volumen, incluso sin agua. [Implementación de referencia de Amulet](https://raw.githubusercontent.com/Amulet-Team/Amulet-Core/1.9.46/amulet/level/formats/mcstructure/format_wrapper.py).

Requisitos del exportador:

- Raíz compound y campos con los tipos NBT verificados en los fixtures.
- `format_version` igual a 1.
- `size` con las tres dimensiones y `structure_world_origin` local.
- Paleta deduplicada con nombre, estados tipados y versión de bloque.
- Dos capas de `block_indices`; la secundaria sin contenido se rellena con `-1`.
- Celda sin escribir: `-1` en la capa primaria. Aire explícito: índice de la entrada aire.
- Recorrido Bedrock: `index = (x * sizeY + y) * sizeZ + z`.
- Entidades vacías y datos de posición vacíos en el alcance inicial.
- Ningún encabezado de `level.dat` ni envoltorio de red añadido al archivo.

El formato v2 será una mejora posterior con sus propios fixtures; no basta con cambiar el número de versión de un archivo v1.

### Pack `.mcpack`

El pack reduce la necesidad de manipular carpetas internas y permite ofrecer la estructura como contenido de un behavior pack.

~~~text
manifest.json
structures/
  aldeano/
    refugio_roble.mcstructure
~~~

El manifiesto tendrá versión de formato estable, header y módulo de tipo `data`, UUID distintos y válidos, versión del pack y `min_engine_version` correspondiente al perfil. No necesita Script API ni resource pack para este MVP. Microsoft documenta las estructuras dentro de behavior packs y los campos del manifiesto. [Contenido de packs](https://learn.microsoft.com/en-us/minecraft/creator/documents/comprehensivepackcontents?view=minecraft-bedrock-stable), [manifiesto](https://learn.microsoft.com/minecraft/creator/reference/content/addonsreference/packmanifest?view=minecraft-bedrock-stable).

Requisitos de empaquetado:

- ZIP con `manifest.json` en la raíz, descargado con extensión `.mcpack`.
- Namespace fijo `aldeano` y nombre saneado del diseño.
- Política de UUID: cada nuevo pack es independiente; al actualizar un proyecto guardado, conservar UUID e incrementar versión.
- Guardar identidad de pack como metadatos locales del proyecto, fuera del JSON que genera la IA.
- Ofrecer el archivo de estructura por separado para Windows.
- Mostrar instrucciones en la respuesta de entrega; no exigir abrir documentación técnica para usarlo.

Guía prevista:

1. Abrir el `.mcpack` con Minecraft y comprobar la importación.
2. Activar el behavior pack en el mundo.
3. Con permisos de comandos, copiar `/structure load aldeano:refugio_roble ~ ~ ~`.

La semántica y permisos de `/structure` se comprobarán en el perfil; Microsoft documenta este comando como ruta de colocación. [Referencia de /structure](https://github.com/MicrosoftDocs/minecraft-creator/blob/main/creator/Reference/Content/CommandsReference/Examples/Commands/structure.md).

Para Windows, ofrecer también la guía corta con `/give @s structure_block`, modo de carga e importación del archivo. En móvil hay que comprobar la asociación de archivos; el comportamiento depende del sistema y su versión.

## 9. Exportación Java

### Estructura NBT nativa

Generar la estructura desde el volumen canónico, serializar NBT big-endian y comprimir con GZIP. La forma exacta se contrastará con una estructura guardada por la versión Java elegida; una extensión `.nbt` correcta no garantiza que el contenido lo sea.

Contrato funcional:

- Tamaño y paleta coherentes con el diseño.
- Lista de bloques con coordenadas locales y referencias de estado válidas.
- Aire explícito incluido y posiciones sin escribir omitidas.
- Entidades vacías y ausencia de NBT arbitrario.
- DataVersion obtenido del perfil, nunca inventado por la IA.
- Una sola paleta suficiente para el MVP.

**No reutilizar sin comprobar el esquema clásico de Java en versiones nuevas.** En Java 26.3 las notas oficiales indican cambios de los campos de Block State de `Name`/`Properties` a `id`/`properties` y una representación compacta del estado predeterminado. Comprobar cómo aparecen en el NBT de estructura guardado por esa versión y adaptar el escritor y lector de pruebas. [Cambios de Java 26.3](https://feedback.minecraft.net/hc/en-us/articles/48913133328013-Minecraft-Java-Edition-26-3).

El fixture y su reimportación resuelven este punto antes de desarrollar el resto del exportador; no es una comprobación que se deja para el final.

### Datapack ZIP listo para instalar

Para el perfil actual, la estructura propuesta del pack es:

~~~text
pack.mcmeta
data/
  aldeano/
    structure/
      refugio_roble.nbt
~~~

La carpeta de datapack es `structure` en singular desde Java 1.21. Esto no permite inferir la ruta de todas las carpetas internas del mundo; el MVP utiliza el datapack para evitar esa confusión. [Cambio oficial de carpetas en Java 1.21](https://www.minecraft.net/en-us/article/minecraft-java-edition-1-21).

`pack.mcmeta` se genera según el perfil. Los formatos recientes introdujeron `min_format` y `max_format`; el valor de formato publicado para Java 26.3 es 121.0. No confundir ese valor con DataVersion ni copiar un `pack_format` antiguo para todas las versiones. [Cambios de metadatos en Java 1.21.9](https://www.minecraft.net/en-us/article/minecraft-java-edition-1-21-9), [formato de Java 26.3](https://feedback.minecraft.net/hc/en-us/articles/48913133328013-Minecraft-Java-Edition-26-3).

Guía prevista:

1. Abrir la carpeta del mundo desde el juego y colocar el ZIP en `datapacks`, con `pack.mcmeta` en la raíz del ZIP.
2. Cargar el mundo o ejecutar `/reload`; verificar que el datapack se reconoce.
3. Copiar `/place template aldeano:refugio_roble ~ ~ ~`, con los permisos necesarios.

El subcomando `place template` coloca una plantilla de estructura; es distinto de generar una estructura de worldgen. [Referencia oficial de /place](https://feedback.minecraft.net/hc/en-us/articles/6731464524941-Minecraft-Java-Edition-1-19).

El `.nbt` suelto queda como descarga avanzada. El generador no debe intentar modificar las carpetas del mundo del suscriptor desde el entorno de la IA.

### `.schem` como mejora posterior

Añadir Sponge Schematic v3 para usuarios que ya utilizan WorldEdit, sin convertirlo en requisito para Java.

La especificación define GZIP/NBT, versión 3, DataVersion, paleta y datos de bloques con índices varint. Su recorrido es `x + z * Width + y * Width * Length`; difiere del recorrido Bedrock. Debe tener un exportador y pruebas propios. [Especificación de Sponge v3](https://github.com/SpongePowered/Schematic-Specification/blob/master/versions/schematic-3.md).

No renombrar `.nbt` a `.schem` ni llamar `.schematic` a los tres formatos.

## 10. Repositorio y archivos entregados

Nombre sugerido: `aldeano-build-generator`.

~~~text
aldeano-build-generator/
├── README.md
├── plan.md
├── LICENSE
├── THIRD_PARTY_NOTICES.md
├── INICIO_IA.md
├── INICIO_IA.txt
├── generator.py
├── instructions/
│   ├── conversation.es.md
│   └── runtime.md
├── schema/
│   └── aldeano-build-v1.schema.json
├── catalog/
│   ├── canonical.json
│   └── profiles/
├── examples/
│   ├── refugio.build.json
│   ├── torre.build.json
│   └── puente.build.json
├── tools/
│   └── build_ai_bundle.py
├── tests/
│   ├── test_validation.py
│   ├── test_volume.py
│   ├── test_bedrock.py
│   ├── test_java.py
│   ├── test_packages.py
│   ├── test_ai_bundle.py
│   └── fixtures/
├── docs/
│   ├── bedrock.md
│   ├── java.md
│   ├── compatibility.md
│   ├── provider-tests.md
│   ├── ai-evaluation.md
│   └── release-checklist.md
└── .github/
    ├── workflows/ci.yml
    └── ISSUE_TEMPLATE/
~~~

El árbol describe archivos futuros. La entrega actual es este plan. El README presentará primero «Usar con una IA»; instalación local y desarrollo irán después.

Funciones previstas:

~~~python
def parse_build(text): ...
def validate_build(data, limits): ...
def compile_volume(build, limits): ...
def resolve_palette(volume, profile): ...
def export_mcstructure(volume, profile): ...
def export_java_structure(volume, profile): ...
def package_bedrock(structure, metadata): ...
def package_java(structure, metadata): ...
def validate_outputs(outputs, profile): ...
~~~

### Archivos de cada construcción

- Pack y archivo de estructura de la edición solicitada.
- `nombre.build.json`.
- `materiales.txt`, sin contar aire como material.
- `validacion.json`: versión del kit, perfil, dimensiones y comprobaciones.
- `LEEME.txt`: pasos y comando.
- Opcional: `preview.svg` de colores propios.

Ofrecer el pack principal como descarga directa. Un ZIP general será opcional; no obligar a descomprimir varios ZIP anidados para encontrar el archivo adecuado.

Respuesta final prevista:

~~~text
He preparado tu casa medieval de 24 × 16 × 20 bloques para Bedrock.

Descargar: casa_medieval.mcpack
También: casa_medieval.mcstructure · design.build.json

Para colocarla:
1. Abre el pack con Minecraft.
2. Actívalo en tu mundo.
3. Con comandos habilitados, utiliza el comando indicado.

Validación del generador: correcta.
~~~

Los enlaces y la validación solo se muestran si existen y se han ejecutado. Una preview no demuestra que el juego acepte el binario.

Para «hazla más alta» o «cambia el tejado», conservar JSON y respuestas, modificar el diseño y recompilar. No repetir el cuestionario.

## 11. Plan de implementación por fases

### Fase 0 — Demostrar ejecución y descarga en cuentas Free

**P0. Antes de invertir en una web o un catálogo grande.**

- [ ] Registrar fecha, cuenta gratuita y superficie de ChatGPT y Claude.
- [ ] Probar lectura de enlace y recepción del texto completo por separado.
- [ ] Crear un binario pequeño y comprobar su descarga real.
- [ ] Verificar Python y módulos estándar.
- [ ] Comprobar acceso remoto a recursos sin asumir que lectura web y ejecución comparten red.
- [ ] Registrar «texto», «archivo directo probado» o «pendiente» por proveedor.
- [ ] Probar que se conservan las respuestas al cambiar de ruta.

Salida: evidencia de las capacidades de cada cuenta. Si falta ejecución en ChatGPT Free, se publica esa limitación y se conserva la ruta textual; no se etiqueta la descarga directa como verificada.

### Fase 1 — Demostrar los formatos en Minecraft

**P0. Puede avanzar mientras se redactan las instrucciones del kit.**

- [ ] Fijar las versiones exactas de ambos juegos.
- [ ] Guardar fixtures propios, pequeños y asimétricos.
- [ ] Inspeccionar NBT, estados y metadatos.
- [ ] Implementar exportadores mínimos de datos propios.
- [ ] Leer los archivos con un lector independiente.
- [ ] Cargarlos realmente en Bedrock y Java.
- [ ] Probar `.mcpack` y datapack y registrar los perfiles.

Salida: escritura → pack → colocación real en ambas ediciones. Si no hay acceso a uno de los juegos, el perfil queda experimental.

### Fase 2 — Compilador reutilizable

**P0. Depende de Fase 1 para sus salidas.**

- [ ] Implementar BuildSpec, límites, alias y materiales.
- [ ] Implementar `set`, `fill` y precedencia.
- [ ] Distinguir aire y omisión.
- [ ] Completar los dos adaptadores y sus packs.
- [ ] Generar materiales, comandos e informe.
- [ ] Mantener cero dependencias de ejecución y cero llamadas de red.
- [ ] Comprobar refugio, torre y puente en ambos juegos.

Salida: un comando genera las salidas de un diseño válido.

### Fase 3 — Instrucciones y paquete de inicio

**P0. Depende de Fase 2 para incluir el compilador.**

- [ ] Escribir preguntas, valores predeterminados y revisiones.
- [ ] Incluir esquema, catálogo, ejemplo y compilador literal.
- [ ] Generar Markdown y texto desde las mismas fuentes.
- [ ] Medir tamaño y eliminar repeticiones.
- [ ] Probar la ejecución después de pegar el paquete, sin acceso a GitHub.
- [ ] Comprobar que la IA utiliza el generador incluido.
- [ ] Preparar respuesta de entrega y recuperación ante falta de herramientas.

Salida: entrada autosuficiente que permite generar sin enseñar programación.

### Fase 4 — Evaluación con IA y suscriptores

**P0. Depende de Fases 0–3.**

- [ ] Ejecutar el corpus en ChatGPT Free y Claude Free.
- [ ] Medir diseño válido, calidad, correcciones y archivo descargado.
- [ ] Probar «decide tú», preferencias completas y revisión posterior.
- [ ] Comprobar respuestas honestas sin ejecución.
- [ ] Evaluar con cinco personas de la comunidad.
- [ ] Verificar Android/iOS antes de etiquetar esas rutas como probadas.
- [ ] Corregir los pasos donde haga falta asistencia.

Salida: matriz pública de cuentas/superficies y experiencia verificadas.

### Fase 5 — Publicación

**P0. Depende de las pruebas del alcance publicado.**

- [ ] Crear repositorio remoto de GitHub.
- [ ] Publicar fuentes, instrucciones, perfiles y ejemplos.
- [ ] Añadir licencia propuesta MIT y avisos de datos/dependencias.
- [ ] CI: pruebas y coherencia del paquete autosuficiente.
- [ ] Publicar release con entrada Markdown/texto y ejemplos.
- [ ] Comprobar enlaces Raw y de release desde una conversación nueva.
- [ ] Grabar tutorial: pegar → responder → descargar → importar.

La implementación y la publicación son posteriores a este documento.

### Fase 6 — Mejoras

Más materiales y estados; operaciones compactas de tejados; preview; Sponge `.schem` v3; Bedrock v2; perfiles anteriores; conversor web opcional y plantillas paramétricas.

No hacer depender el kit conversacional de estas mejoras.

## 12. Pruebas y objetivos de aceptación

Estas pruebas se planifican aquí; todavía no se han ejecutado.

### Compilador

- `fill` [0,0,0] → [1,1,1] contiene ocho posiciones.
- Última escritura gana.
- Aire explícito vacía; omisión conserva.
- Coordenadas, alias, campos y materiales inválidos se rechazan.
- Los límites se aplican antes de expandir.
- Se calcula el presupuesto de todas las escrituras, incluidas las superpuestas.
- Un JSON incompleto no genera descarga presentada como válida.

### Binarios y packs

- Lector independiente del escritor, además de pruebas unitarias.
- Verificar endian, compresión, tipos, paletas y dimensiones.
- Figura asimétrica para detectar intercambio de ejes.
- Casos de omisión, aire y bloques en las esquinas.
- Ambas capas correctas para Bedrock v1.
- Esquema exacto de la versión Java objetivo.
- Metadatos/manifiesto en la raíz del ZIP y rutas correctas.
- Comparar semántica; timestamps y UUID no deben volver frágiles las pruebas.

### Dentro del juego

| Caso | Bedrock Windows | Java escritorio |
| --- | --- | --- |
| Refugio | Carga e interior útil | Carga e interior útil |
| Figura asimétrica | Ejes y origen correctos | Ejes y origen correctos |
| Torre y puente | Geometría y materiales | Geometría y materiales |
| Aire sobre terreno | Vacía donde corresponde | Vacía donde corresponde |
| Omisión | Conserva terreno | Conserva terreno |
| Pack | Importar, activar y colocar | Reconocer y colocar |

Registrar versión, SO, archivo y resultado. Una captura de preview no sustituye estas pruebas.

### Paquete y conversación

- El compilador incluido coincide con la release.
- Todos los recursos mínimos están en el paquete.
- Compila sin paquetes externos ni red.
- Texto y Markdown contienen el mismo kit.
- Probar pegado del enlace separadamente del texto completo.
- No confundir una instrucción aceptada con un generador ejecutado.

Corpus: diez peticiones en español, dos intentos por petición y proveedor, hasta 40 generaciones repartidas dentro de las cuotas normales.

Incluir casa, torre, puente, templo, medidas inválidas, ambas ediciones, «decide tú», revisión y falta de herramientas.

Objetivos propuestos:

- Una ronda normal de preguntas; otra solo por incompatibilidad o ambigüedad necesaria.
- 90 % de diseños válidos inicialmente; 95 % tras una corrección.
- Cero enlaces inventados o falsas afirmaciones de ejecución en los casos evaluados.
- Todos los archivos entregados como válidos pasan el validador.
- Tres ejemplos curados cargados en ambos juegos.
- Cuatro de cinco participantes completan el flujo sin asistencia.

Cada etiqueta «descarga directa verificada en Free» exige una prueba completa en la cuenta/superficie correspondiente. Publicar fecha y condiciones; no generalizar a todas las cuentas.

## 13. Alternativas, coste y distribución

### No puede leer GitHub

Pegar el paquete completo o adjuntar texto si la sesión lo permite. Conservar las preferencias ya aportadas.

### Puede diseñar pero no ejecutar

Entregar BuildSpec completo y explicar que todavía no existe un binario. Rutas disponibles:

1. Continuar con kit y diseño en una sesión con ejecución.
2. Usar un conversor web únicamente cuando ya se haya implementado y publicado.

No enlazar una web imaginaria. Documentar ejecución local como opción avanzada, sin convertirla en requisito para todos.

### Cuota o adjuntos limitados

Permitir guardar diseño y respuestas para continuar después. Si una extensión se rechaza, probar un ZIP que contenga el archivo conservando su formato. Registrar esa alternativa en el proveedor objetivo.

### Coste

| Parte | Propuesta |
| --- | --- |
| Código e instrucciones | GitHub público y releases |
| Inferencia | Cuenta del suscriptor, con sus límites |
| Compilación | Entorno de código de la conversación |
| Hosting propio | No obligatorio en v1.0 |
| Juego | Minecraft adquirido por el usuario |

No pagar API central ni usar GitHub Actions como servidor de generación por suscriptor. CI solo prueba y prepara el kit.

«Gratuito» no significa ilimitado o permanente. Reducir el kit y el diseño ayuda a aprovechar las cuotas.

## 14. Riesgos, privacidad y mantenimiento

| Riesgo | Respuesta |
| --- | --- |
| La URL no proporciona todos los archivos | Entrada autosuficiente |
| El chat genera texto pero no ejecuta | Detectar capacidades y conservar diseño |
| La IA reinventa el compilador | Incluir código probado y registrar qué se ejecutó |
| El paquete consume mucho contexto | Perfiles mínimos y tamaño medido |
| Estados distintos entre ediciones | Catálogo canónico y mapeos verificados |
| Cambios de Java o Bedrock | Fixtures y adaptadores por versión |
| Nuestro lector acepta un archivo que el juego rechaza | Lector independiente y carga real |
| Construcción válida pero pobre | Ejemplos curados y evaluación humana |
| Expectativas de importación en consola | Matriz de plataformas visible |
| Cambia la disponibilidad de herramientas gratuitas | Pruebas fechadas y ruta textual |

La descripción y el diseño se procesan en el proveedor elegido. No afirmar que toda la conversación permanece únicamente en el dispositivo.

El compilador no necesita enviar datos a un servidor del creador. Usar colores y ejemplos propios y documentar licencias de código y datos.

Mantenimiento: revisar perfiles con actualizaciones del juego, conservar fixtures pequeños propios, separar cambios de BuildSpec de cambios de Minecraft, regenerar los paquetes y repetir la prueba real antes de marcar un perfil como verificado.

## 15. Criterio de finalización y orden de trabajo

- [ ] README orientado a usar el repositorio con una IA.
- [ ] Entrada autosuficiente en Markdown y texto.
- [ ] Cuatro preguntas como máximo, agrupadas y con valores predeterminados.
- [ ] Compilador incluido, reproducible y sin dependencias de ejecución.
- [ ] Un mismo diseño produce Bedrock y Java.
- [ ] Archivos y packs cargados realmente en ambos juegos.
- [ ] Descarga directa probada en al menos un proveedor gratuito.
- [ ] Matriz explícita del estado de ChatGPT Free y Claude Free.
- [ ] Nunca presentar texto como binario terminado.
- [ ] JSON reutilizable, materiales, informe e instrucciones.
- [ ] Revisiones sin repetir preguntas ya respondidas.
- [ ] Tres ejemplos y tutorial corto publicados.
- [ ] Evaluación con cuentas Free y suscriptores registrada.

Orden recomendado:

1. Probar ejecución y descarga en las cuentas objetivo.
2. Generar estructuras mínimas aceptadas en Bedrock y Java.
3. Completar compilador y contrato pequeño.
4. Empaquetar instrucciones, catálogo y compilador.
5. Evaluar con IA y comunidad.
6. Publicar el repositorio y su matriz de capacidades verificadas.
7. Añadir mejoras según resultados.

La experiencia deseada es **«presento el kit, respondo unas preguntas y recibo mi construcción»**. Para afirmarla en un proveedor concreto, hay que haber probado su ruta completa de descarga.
