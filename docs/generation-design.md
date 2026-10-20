# Método de generación de v0.2

La mejora combina una gramática de construcción manual, componentes reutilizables,
estados de bloques contrastados y revisión previa a la entrega.

## Investigación utilizada

[APT](https://arxiv.org/abs/2411.17255) estudia planificación arquitectónica y
descomposición de construcciones, con mecanismos de revisión y reutilización.
Aquí se adopta una secuencia breve de composición, construcción y revisión.

[T2BM](https://arxiv.org/abs/2406.08751) estudia generación de edificios con
representaciones intermedias y reparación. Aquí la IA produce una solicitud o
BuildSpec; el compilador valida geometría y formatos antes de entregar.

[SIGI](https://computationalcreativity.net/iccc21/wp-content/uploads/2021/09/ICCC_2021_paper_29.pdf)
estudia gramáticas de formas extraídas de ejemplos voxel. En este proyecto las
reglas son manuales y el ejemplo inicial es una posada propia.

Estas fuentes motivan decisiones de diseño. Los resultados de sus experimentos
no son resultados medidos para este kit o para las cuentas gratuitas del usuario.

## Implementación

1. Composición: volúmenes, proporciones, alturas, acceso y paleta.
2. Componentes: habitaciones vaciadas, cubiertas con aleros/cumbrera, ventanas,
   vigas y detalles. Builder permite usar estas piezas en diseños libres.
3. Dos rutas: solicitud compacta de posada o BuildSpec libre.
4. Exportación desde un mismo volumen a Bedrock y Java.
5. Diagnósticos de aire, paleta y espacio cubierto; revisión de la vista 3D.
6. Corrección de problemas detectados antes de adjuntar el resultado.

La solicitud de posada ocupa pocas líneas; su expansión produce cientos de
operaciones sin pedir al modelo que las escriba una por una.
La plantilla tiene tamaño fijo 31 × 32 × 29 y tres paletas.
No sirve como plantilla universal de todos los edificios.

El kit completo crece por incluir los componentes y renderizador.
Para aprovechar la ejecución del chat, se extraen los dos archivos del adjunto
por programa; la IA evita volver a emitir miles de tokens de código.
Esto reduce salida repetida, pero no elimina las cuotas del proveedor.

## Límites de la revisión

revision.json ofrece diagnósticos; no asigna una nota de belleza.
El espacio cubierto se calcula por celdas. No simula puertas, colisiones parciales,
redstone, iluminación o navegación real del jugador.
La inspección visual y la prueba dentro del juego siguen siendo necesarias.

Hay pruebas automatizadas y datos cotejados de los estados incorporados.
Falta la comparación con usuarios y cuentas Free para medir cuántos resultados
nuevos cumplen el estilo solicitado y cuánto mejora su calidad.
