# Resultados locales de v0.2.1

Fecha: 20 de octubre de 2026. Entorno: Windows, Python 3.14.7.

- 52 pruebas automatizadas correctas.
- NBT Bedrock y Java leídos con nbtlib 2.0.4 como lector independiente.
- Ejemplos válidos contra JSON Schema con jsonschema 4.26.0.
- Volumen máximo probado: 48³, 110.592 bloques.
- Kit extraído y ejecutado desde una carpeta temporal sin repositorio y con python -S.
- 82 alias y variantes de materiales cotejados con datos de bloques Bedrock 1.26.30 y Java 26.3/1.21.1.
- Paquete de inicio autosuficiente regenerado con las instrucciones de entrega y verificación.
- Cuatro ejemplos generados con ambas ediciones y previews SVG.

No realizado: carga dentro de Minecraft ni conversación real con cuentas gratuitas.
Las pruebas de formato no sustituyen esas comprobaciones.
GitHub Actions no activado: el token de publicación no tiene scope workflow.
La plantilla se conserva en .github/ci-template.yml.

Incluye pruebas de todos los temas, elementos opcionales, puertas emparejadas,
estados detallados, geometría parcial y ejecución aislada de la solicitud compacta.

## Investigación del aviso de corrupción en un visor web

No se dispone del visor o archivo exactos que produjeron el aviso. Se han revisado
los cuatro ejemplos publicados en v0.2.0: ocho binarios, contando Java y Bedrock.
También se han generado doce binarios nuevos: cuatro Bedrock y cuatro por cada
perfil Java. Los 20 pasan lectura independiente y reescritura con bytes idénticos
en **nbtlib 2.0.4** y **prismarine-nbt 2.8.0**.

Esto demuestra que esos archivos están bien formados y son legibles por ambos
parsers. No permite atribuir el aviso a una causa concreta. Un visor de estructuras
puede necesitar Name/Properties, otro formato o una versión distinta.
Los ejemplos nuevos usan como base Java 1.21.1; la CLI exige seleccionar perfil.

Se conservan nombres, tamaños y SHA-256 en [el informe de integridad](integrity-v0.2.1.json).

Se añaden pruebas de CRC GZIP alterado, cabeceras inválidas, truncamiento, bytes
sobrantes, miembros GZIP concatenados, texto renombrado, endian incorrecto,
tipos NBT incorrectos, índices fuera de paleta, coordenadas inválidas o duplicadas,
perfil equivocado, entrega mínima y daño simulado después de escribir al disco.
Los fallos impiden anunciar una entrega correcta.

Para repetir la comprobación con ambos lectores:

~~~text
python -m pip install -r requirements-dev.txt
npm install --prefix .cache/nbt-check --ignore-scripts --no-audit --no-fund prismarine-nbt@2.8.0
python tools/build_integrity_fixtures.py --baseline v0.2.0
python tools/check_nbtlib.py .cache/integrity/manifest.json
node tools/check_prismarine.cjs .cache/integrity/manifest.json
~~~

Node y las bibliotecas independientes solo se necesitan para estas pruebas de
desarrollo; el kit de los suscriptores sigue usando únicamente Python estándar.
Referencia del segundo lector: [PrismarineJS/prismarine-nbt](https://github.com/PrismarineJS/prismarine-nbt).
