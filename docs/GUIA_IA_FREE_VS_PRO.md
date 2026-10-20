# Guía de Uso: IA Tier Free vs IA de Pago (Code Interpreter)

Aldeano Build Generator está optimizado para que cualquier usuario, sin importar qué herramienta o suscripción de Inteligencia Artificial tenga, pueda obtener construcciones excepcionales y colocarlas en su mundo de Minecraft.

---

## 📊 1. Matriz de Capacidades por Plataforma de IA

| Plataforma / Nivel | Herramientas en el Chat | ¿Ejecuta Python? | ¿Qué entrega la IA? |
| :--- | :--- | :---: | :--- |
| **ChatGPT Plus / Team / Pro** | Python Sandbox (Code Interpreter / Advanced Data Analysis) | ✅ Sí | Enlaces de descarga directa de `.mcstructure`, `.nbt`, `.datapack.zip` y `.mcpack`. |
| **Claude Pro / Max** | Analysis Tool / Artifacts interactivos | ✅ Sí (con límites) | Archivos de estructura o Artifact interactivo con visor de planos. |
| **ChatGPT Free (con cuota)** | Cuotas periódicas de análisis de archivos | ⚠️ Parcial | Si dispone de cuota de Python, entrega binarios. Si se agota, entrega diseño JSON. |
| **Claude Free** | Artifacts de solo lectura (HTML/SVG/React) | ❌ No | Artifact interactivo con visor 3D + diseño JSON + comando de compilación local. |
| **Gemini / DeepSeek / Copilot** | Chat de texto puro | ❌ No | Diseño JSON validado + lista de materiales en stacks + guía de capas para supervivencia. |

---

## 🚀 2. Flujo Óptimo para IAs con Intérprete de Código (Tier de Pago)

Si tienes **ChatGPT Plus** o una IA con entorno Python activo:

1. Inicia una nueva conversación.
2. Descarga el kit completo: **[INICIO_IA.txt](https://raw.githubusercontent.com/Aldeanoo/aldeano-build-generator/v0.2.1/INICIO_IA.txt)** y **adjúntalo como archivo** en el chat.
3. Copia el mensaje inicial de **[MASTER_PROMPT.md](../MASTER_PROMPT.md)** o escribe:
   > *"Usa el kit adjunto para ayudarme a construir un castillo con torres y foso para Bedrock y Java."*
4. La IA extraerá los módulos en segundo plano, ejecutará el compilador, verificará los archivos binarios y te entregará:
   - 📥 Enlace de descarga directa de `<nombre>.mcstructure`.
   - 📥 Enlace de descarga directa de `<nombre>.nbt`.
   - 📥 Enlace de descarga directa de `<nombre>.datapack.zip`.
5. Descarga los archivos y sigue la **[Guía de Importación](GUIA_DE_IMPORTACION.md)** para colocarlos en tu mundo.

---

## 💡 3. Flujo Óptimo para IAs Gratuitas (Tier Free / Solo Texto)

En una IA gratuita sin acceso a terminal o ejecución de código Python:

1. Abre tu IA de chat favorita (**ChatGPT Free, Claude Free, Gemini, DeepSeek, etc.**).
2. Abre **[MASTER_PROMPT.md](../MASTER_PROMPT.md)**, copia el bloque completo y pégalo en el chat.
3. Pídele directamente lo que quieras construir (ejemplo: *"Quiero un faro costero nórdico de 15x15 con mirador y linterna"*).
4. La IA aplicará las **Reglas de Calidad Arquitectónica** (zócalos de piedra, pilares esquineros salientes, tejados con aleros, puertas pareadas) y te entregará:
   - ✅ **Diseño en JSON validado:** Un bloque de código con el esquema `"aldeano-build/v1"`.
   - 📦 **Lista de Materiales en Stacks:** Número exacto de cofres y stacks necesarios para conseguir los bloques en modo Supervivencia.
   - 📐 **Plano por Capas:** Desglose piso por piso (Cimientos, Planta Baja, Primera Planta, Tejado).
5. **Cómo compilar los archivos descargables en tu PC en 1 segundo:**
   - Guarda el JSON de la IA como `diseno.build.json`.
   - Descarga únicamente el archivo `generator.py` de este repositorio.
   - Abre la consola (Terminal en Windows/Mac/Linux) y ejecuta:
     ```bash
     python generator.py diseno.build.json --delivery structures --java-profile java-1.21.1
     ```
   - **¡Cero dependencias externas!** No necesitas instalar pip, ni librerías de terceros. En 0.1 segundos tendrás tus archivos `.mcstructure` y `.nbt` listos en tu carpeta.
