# Probar en Java

| Perfil | DataVersion | Datapack | Paleta |
| --- | --- | --- | --- |
| java-26.3 | 5023 | min/max 121.0 | id / properties |
| java-1.21.1 | 3955 | pack_format 48 | Name / Properties |

Perfiles experimentales: binarios contrastados con nbtlib; falta colocación en Minecraft.
La CLI exige perfil explícito. La API Python usa la base 1.21.1 si no se indica otro.
Los ejemplos de v0.2.1 usan 1.21.1; los de v0.2.0 usaban 26.3.

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

## Solo el .nbt y comprobación de integridad

~~~text
python generator.py examples/posada.request.json --delivery nbt --java-profile java-1.21.1 --output output-java121
python generator.py --verify output-java121/posada_del_roble.nbt --java-profile java-1.21.1
~~~

La carpeta contiene únicamente el `.nbt`. La verificación sale por consola.
Para cargarlo como estructura guardada, cópialo a
`generated/aldeano/structures/posada_del_roble.nbt` dentro de tu mundo.
En un bloque de estructura Java, modo Cargar, usa `aldeano:posada_del_roble`.
La carga real sigue pendiente de prueba.

Este archivo es una estructura vanilla: no un `.schem`, `.schematic` ni `.litematic`.
El visor debe admitir GZIP, NBT big-endian y las claves de paleta del perfil elegido.
Un visor que espera `Name` podría rechazar la paleta `id` de 26.3 aunque el NBT sea
legible. Es una explicación posible; sin el visor y archivo concretos no se puede
atribuirle el error comunicado.

`--verify` detecta errores de CRC, truncamiento, bytes sobrantes, tipos NBT,
paletas, posiciones e índices incorrectos y discrepancias de perfil. Es estricto
para las salidas de este generador, no un importador universal de NBT ajenos.
Véanse [las pruebas con dos lectores independientes](test-results.md).
