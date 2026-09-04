# NanoClase

Convierte un documento docente en una clase de tres minutos. Evalúa el material,
lo reescribe, vuelve a evaluarlo para que veas qué ha cambiado, y monta un vídeo
locutado con el texto leído escrito debajo de cada diapositiva. Puede empezar en un
idioma y terminar en otro.

Todo ocurre en el navegador. No hay servidor: el documento no sale del ordenador salvo
en las llamadas a la API de OpenAI.

**Aplicación**: https://fborrasumh.github.io/nanoclase/

## El recorrido

1. **Clave, modelos e idiomas.** El idioma de entrada se detecta solo; el de salida lo
   eliges de una lista de treinta y dos, o lo escribes. El documento reescrito y el
   vídeo salen en ese idioma.
2. **El documento.** `.ipynb`, `.docx`, `.pdf` con texto seleccionable, `.md`, `.txt`.
3. **Cómo está ahora.** Ocho dimensiones puntuadas de 0 a 10: objetivos observables,
   requisitos previos, estructura, entrada y salida de cada bloque, comprobaciones de
   comprensión, ejemplos, claridad y cierre. Con lo que falta, lo que funciona y la
   única cosa que más mejoraría el documento.
4. **La reescritura.** Toma como encargo las carencias de la evaluación anterior. Sale
   en Markdown y, si la entrada era un cuaderno, también en `.ipynb`.
5. **Qué ha cambiado.** La misma rúbrica sobre el resultado, junto a la de partida y
   con la diferencia por dimensión. Una dimensión que no sube es una que la reescritura
   no ha tocado.
6. **El guion y las diapositivas.** Eliges el número de diapositivas, que es lo que fija
   la duración: unos 22 segundos cada una. Se retoca escena a escena o editando el JSON
   entero, que se valida antes de redibujar.
7. **La voz y el montaje.** Una llamada de voz por escena, y las duraciones reales de
   cada audio son las que sincronizan diapositivas y texto.

## El texto bajo la diapositiva

La franja inferior de cada diapositiva lleva escrito lo que se está oyendo, troceado en
fragmentos de menos de cien caracteres para que quepa en dos líneas. Está pensado para
quien no oye, para quien ve el vídeo sin sonido y para quien sigue una clase en un
idioma que no es el suyo. Se puede desactivar y dejar el texto solo en el `.srt`.

## El formato del vídeo

El navegador graba en **WebM**. Es lo que se puede montar sin servidor: el MP4 exigiría
`ffmpeg.wasm` con `SharedArrayBuffer`, que necesita cabeceras HTTP que GitHub Pages no
permite fijar. WebM se ve en cualquier navegador y en Moodle.

Para MP4, descarga el zip y ejecuta las órdenes de `montar_mp4.txt`. Las diapositivas
del zip llevan la franja vacía y ffmpeg escribe el texto encima desde el `.srt`, así que
el resultado es equivalente. Las duraciones vienen calculadas: sale sincronizado sin
tocar nada.

## Coste

Con `gpt-4.1-mini` y `gpt-4o-mini-tts`, las dos evaluaciones, la reescritura, el guion y
un vídeo de tres minutos rondan los **quince céntimos**. Se factura en tu cuenta de OpenAI.

## La clave

Se guarda en `localStorage` con la llave `ia_openai_key` y viaja solo a `api.openai.com`.
No la uses en un ordenador compartido; el botón «Olvidarla» la borra.

## Navegadores

Chrome, Edge y Firefox montan el vídeo. Safari lee documentos y genera la voz, pero su
grabador es irregular: ahí conviene la ruta del zip. Mientras se graba, la pestaña tiene
que quedarse delante: el navegador congela el dibujado en segundo plano y el vídeo
saldría a saltos.

## Licencia

CC BY-SA 4.0.
