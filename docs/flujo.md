# Flujo del suscriptor

## 1. Iniciar

Adjunta INICIO_IA.txt v0.2.0 y escribe:

~~~text
Usa el kit adjunto para generar una construcción detallada de Minecraft.
Pregúntame solo lo que falte y luego genera los archivos.
~~~

También puedes pegar:

~~~text
Lee y utiliza este kit:
https://raw.githubusercontent.com/Aldeanoo/aldeano-build-generator/v0.2.0/INICIO_IA.txt
Quiero una construcción detallada. Hazme las preguntas necesarias y genera
los archivos usando el código del kit.
~~~

Si no puede leer la URL, adjunta el TXT o pega su contenido completo.
Si ya tenías una conversación con v0.1.0, adjunta el archivo nuevo y pide que
sustituya architect.py y generator.py por los de v0.2.0.

## 2. Preguntas de la IA, en un mensaje

- ¿Qué construcción y estilo quieres?
- ¿Bedrock, Java o ambos? ¿Dispositivo y versión?
- ¿Qué tamaño o espacio tienes?
- ¿Qué detalles o interiores necesitas?

Puede omitir lo que ya sepa. Puedes decir «decide tú».

Ejemplo de respuesta:

~~~text
Una posada medieval con mucho detalle, para Bedrock en Windows.
Tengo espacio de 32 × 32 × 32. Quiero balcón, chimenea, buhardilla,
jardín e interior. Usa roble, vigas oscuras y cubierta de pizarra.
~~~

## 3. Generación

La IA resume en una frase el diseño y continúa.
Para este encargo utiliza la posada incluida y la personaliza.
Internamente prepara la solicitud, ejecuta, revisa diagnósticos y preview,
y corrige los problemas que detecte. No necesita otra aprobación.

Para otras construcciones usa Builder o BuildSpec libre con sus componentes.
No debe convertir una petición de castillo o nave en la misma posada.

## 4. Entrega

Recibes:
- Preview isométrica.
- Pack/estructura de la edición elegida.
- Solicitud o diseño JSON para cambios.
- Pasos y comando para colocarlo en el mundo.

«Haz el tejado de madera y quita la chimenea» se resuelve cambiando la solicitud
y regenerando, sin repetir el cuestionario.

Crear archivos necesita ejecución de código en esa sesión. Si falta, la IA
debe conservar el diseño y explicar qué queda por convertir.
Los perfiles siguen pendientes de prueba dentro de Minecraft.
