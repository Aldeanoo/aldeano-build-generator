# Probar en Bedrock

Perfil experimental: datos 1.26.30 y mcstructure v1 sin compresión.
La carga dentro del juego todavía está pendiente.

## Windows

1. Descarga casa_medieval.mcstructure de samples/casa_medieval.
2. En un mundo creativo de ensayo con comandos, ejecuta `/give @s structure_block`.
3. Coloca el bloque, cambia a Cargar, importa el archivo y pulsa Cargar.

El botón de importación requiere Windows y ser anfitrión.
[Microsoft: estructuras](https://learn.microsoft.com/en-us/minecraft/creator/documents/structures/introductiontostructureblocks?view=minecraft-bedrock-stable).

## Pack

1. Abre casa_medieval.mcpack con Minecraft.
2. Activa el behavior pack en el mundo.
3. Con permisos, ejecuta `/structure load aldeano:casa_medieval ~ ~ ~`.

Android/iOS: asociación e importación pendientes por sistema. Consola sin ruta directa prometida.
Actualizar el mismo nombre conserva UUID; incrementa `--pack-version 1.0.1`.
Si falla, registra versión exacta, plataforma, mensaje y archivo.
