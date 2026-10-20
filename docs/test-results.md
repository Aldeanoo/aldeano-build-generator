# Resultados locales de v0.2.0

Fecha: 20 de octubre de 2026. Entorno: Windows, Python 3.14.7.

- 40 pruebas automatizadas correctas.
- NBT Bedrock y Java leídos con nbtlib 2.0.4 como lector independiente.
- Ejemplos válidos contra JSON Schema con jsonschema 4.26.0.
- Volumen máximo probado: 48³, 110.592 bloques.
- Kit extraído y ejecutado desde una carpeta temporal sin repositorio y con python -S.
- 82 alias y variantes de materiales cotejados con datos de bloques Bedrock 1.26.30 y Java 26.3/1.21.1.
- Paquete de inicio: 16.908 tokens con o200k_base (estimación específica de ese tokenizador).
- Cuatro ejemplos generados con ambas ediciones y previews SVG.

No realizado: carga dentro de Minecraft ni conversación real con cuentas gratuitas.
Las pruebas de formato no sustituyen esas comprobaciones.
GitHub Actions no activado: el token de publicación no tiene scope workflow.
La plantilla se conserva en .github/ci-template.yml.

Incluye pruebas de todos los temas, elementos opcionales, puertas emparejadas,
estados detallados, geometr?a parcial y ejecuci?n aislada de la solicitud compacta.
