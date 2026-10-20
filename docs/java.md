# Probar en Java

| Perfil | DataVersion | Datapack | Paleta |
| --- | --- | --- | --- |
| java-26.3 (predeterminado) | 5023 | min/max 121.0 | id |
| java-1.21.1 | 3955 | pack_format 48 | Name |

Perfiles experimentales: binarios contrastados con nbtlib; falta colocación en Minecraft.

1. Copia nombre.datapack.zip dentro de datapacks/ de la carpeta del mundo.
2. Carga el mundo o ejecuta `/reload`. Comprueba `/datapack list`.
3. Con permisos, ejecuta `/place template aldeano:casa_medieval ~ ~ ~`.

Sustituye casa_medieval por tu diseño. No uses el ZIP general .todo.zip como datapack.
No extraigas el datapack: pack.mcmeta está en su raíz.

Para Java 1.21.1:

~~~text
python generator.py examples/casa_medieval.build.json --edition java --java-profile java-1.21.1 --output output-java121
~~~

No basta cambiar la extensión o los metadatos para convertir formatos.
Si falla, registra mensaje, versión y perfil.
