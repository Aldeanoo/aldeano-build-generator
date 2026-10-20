# Guía Universal de Importación en Minecraft

Esta guía explica, paso a paso y de manera visual, cómo importar y colocar tu construcción generada dentro de tu mundo de Minecraft, tanto en **Bedrock Edition** (Windows, Android, iOS y Consolas) como en **Java Edition**.

---

## 🧭 1. Identifica qué archivo tienes

| Archivo | Edición | Método Recomendado | Requisitos |
| :--- | :--- | :--- | :--- |
| **`.mcstructure`** | Bedrock | Bloque de estructura nativo | Windows 10/11 con Trucos activos. |
| **`.mcpack`** | Bedrock | Doble clic / Abrir con Minecraft | Móvil (Android/iOS) y PC. Activar en ajustes del mundo. |
| **`.datapack.zip`** | Java Edition | Carpeta `datapacks/` del mundo | Java 1.21.1+ vanilla. No requiere mods. |
| **`.nbt`** | Java Edition | Bloque de estructura vanilla | Java 1.21.1+ colocado en `generated/aldeano/structures/`. |
| **`.todo.zip`** | Ambas | Paquete completo | Contiene todas las estructuras, vistas previas y guías. |

---

## 🟩 2. Minecraft Bedrock Edition

### Método A: En Windows con Bloque de Estructura (El más directo con `.mcstructure`)
1. Entra a tu mundo de Minecraft en Windows 10/11 (asegúrate de que los **Trucos estén activados** en los Ajustes del Mundo).
2. Abre el chat (`T` o Enter) y obtén un bloque de estructura:
   ```text
   /give @s structure_block
   ```
3. Coloca el bloque en el suelo en el punto donde quieras que empiece la esquina de tu construcción.
4. Haz clic derecho sobre el bloque de estructura para abrir su menú:
   - Cambia el modo en la esquina superior izquierda de **Guardar** a **Cargar** (Load).
   - Haz clic en el botón **Importar** (arriba a la derecha).
   - En el explorador de archivos, selecciona tu archivo descargado `<nombre>.mcstructure`.
5. Verás el contorno tridimensional de la estructura en tu pantalla. Ajusta las coordenadas o rotación si lo deseas.
6. Pulsa el botón **Cargar** en la parte inferior. ¡Tu construcción aparecerá al instante!

---

### Método B: En Móvil (Android, iPhone, iPad) y PC con `.mcpack`
1. Descarga el archivo `<nombre>.mcpack` en tu dispositivo.
2. Abre el archivo:
   - **En Android / iOS:** Toca el archivo descargado desde tu navegador o explorador de archivos y selecciona **"Abrir con Minecraft"**.
   - **En Windows:** Haz doble clic sobre el archivo `.mcpack`.
3. Minecraft se abrirá automáticamente y mostrará las notificaciones:
   - *"Importación iniciada..."*
   - *"Importación de <nombre> completada con éxito."*
4. En el menú de Minecraft:
   - Ve a tus mundos y pulsa el icono del lápiz (**Editar**) en el mundo donde quieras colocar la construcción (o crea un mundo nuevo).
   - Desplázate en el menú lateral izquierdo hasta **Paquetes de comportamiento (Behavior Packs)**.
   - En la pestaña **Mis paquetes**, localiza tu construcción y pulsa **Activar**.
5. Entra a tu mundo y escribe en el chat:
   ```text
   /structure load aldeano:<nombre_construccion> ~ ~ ~
   ```
   *(Ejemplo: `/structure load aldeano:posada_del_roble ~ ~ ~`)*.

> [!NOTE]
> **Consolas (PlayStation, Xbox, Nintendo Switch):**  
> Las consolas no admiten descarga directa de archivos desde el navegador. La forma universal de importar construcciones a consolas es importar el mundo primero en PC o Móvil (mediante `.mcpack` o `.mcstructure`) y luego jugarlo en la consola mediante una suscripción de **Minecraft Realms** o en una partida en red local (**LAN**).

---

## ☕ 3. Minecraft Java Edition

### Método A: Datapack Vanilla (Recomendado con `.datapack.zip`)
*No requiere Forge, Fabric ni ningún mod instalado.*

1. Localiza la carpeta de tu mundo:
   - En Windows, pulsa `Win + R`, escribe `%appdata%\.minecraft\saves` y pulsa Enter.
   - Entra en la carpeta correspondiente a tu mundo.
   - Entra en la subcarpeta `datapacks/`.
2. Copia dentro el archivo `<nombre>.datapack.zip` (¡tal cual, comprimido en ZIP!).
3. Entra a tu mundo en Minecraft (o si ya estabas dentro, escribe en el chat `/reload`).
4. Sitúate donde quieras colocar la construcción y ejecuta:
   ```text
   /place template aldeano:<nombre_construccion> ~ ~ ~
   ```
   *(Ejemplo: `/place template aldeano:posada_del_roble ~ ~ ~`)*.

---

### Método B: Bloque de Estructura nativo con `.nbt`
1. En la carpeta de tu mundo (`%appdata%\.minecraft\saves\<TuMundo>`), crea la siguiente estructura de carpetas si no existe:
   ```text
   generated/aldeano/structures/
   ```
2. Coloca tu archivo `<nombre>.nbt` dentro de esa carpeta `structures/`.
3. En el juego, obtén un bloque de estructura:
   ```text
   /give @s structure_block
   ```
4. Colócalo en el suelo, haz clic derecho, cambia al modo **Cargar**, y en el campo de texto escribe:
   ```text
   aldeano:<nombre_construccion>
   ```
5. Pulsa **Cargar**.

---

## ❓ 4. Preguntas Frecuentes y Solución de Problemas

### 🔹 "El comando dice que la estructura no existe o no se encuentra"
- **En Java:** Asegúrate de haber ejecutado `/reload` o de haber reiniciado el mundo tras colocar el `.datapack.zip`.
- **En Bedrock:** Asegúrate de haber activado el paquete de comportamiento en los ajustes del mundo *antes* de entrar a la partida.

### 🔹 "La construcción apareció enterrada o flotando en el aire"
Las coordenadas relativas `~ ~ ~` sitúan la esquina inferior de la construcción a la altura de tus pies:
- Si quieres que aparezca un bloque por encima del suelo, usa: `~ ~1 ~`.
- Si quieres que los cimientos queden enterrados 1 bloque, usa: `~ ~-1 ~`.

### 🔹 "¿Por qué un visor web de NBT dice que el archivo está dañado?"
Nuestros archivos `.nbt` y `.mcstructure` son **100% nativos del motor oficial de Mojang**:
- El `.nbt` de Java está comprimido con GZIP estándar y utiliza las etiquetas oficiales de Mojang (`size`, `palette`, `blocks`, `DataVersion`).
- Muchos visores web no oficiales esperan archivos `.schematic` (antiguo formato de WorldEdit) o `.litematic` (mod Litematica), que son formatos de mods completamente distintos a las estructuras oficiales de Minecraft.
- Cada archivo generado por Aldeano Build Generator se verifica mediante lectura binaria estricta con las librerías independientes `nbtlib` y `prismarine-nbt`.
