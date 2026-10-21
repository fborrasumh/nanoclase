# NanoClase

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22300395.svg)](https://doi.org/10.5281/zenodo.22300395)

**Aplicación:** https://fborrasumh.github.io/nanoclase/

Crea o mejora un **material docente** y genera, a partir de él, todo lo que necesita una clase universitaria. Está pensada para el profesorado universitario iberoamericano. Aplicación de un solo fichero, sin servidor: todo ocurre en el navegador con tu clave de OpenAI.

## Novedades de la versión 2.1: figuras y fórmulas

- **Lectura con imágenes y ecuaciones.** Del PDF se extraen las imágenes incrustadas; del Word, las imágenes y las ecuaciones nativas, que pasan a LaTeX sin IA; del **PowerPoint** (nuevo formato de entrada), las imágenes, las ecuaciones y las notas del ponente; del cuaderno, las salidas gráficas. Los logotipos que se repiten en cada página se descartan solos.
- **Galería** donde el profesor decide qué usar, marca lo importante y corrige el pie, el texto alternativo y la fuente o licencia de cada figura.
- **Recorte sobre la página** del PDF o sobre cualquier imagen, para las figuras vectoriales y las fórmulas que no son imágenes. El texto roto que queda dentro del recorte deja de leerse como texto.
- **Fórmulas a LaTeX** con el modelo de visión de OpenAI, con el recorte y el LaTeX compilado uno al lado del otro y la lectura en voz alta de cada fórmula.
- **Material, guion y revisores conscientes de las figuras**: la reescritura conserva cada figura y cada fórmula; el guion decide en qué diapositiva va cada una y dice las fórmulas con palabras; el revisor compara cada LaTeX con su recorte y avisa si falta una figura importante.
- **Plantillas de diapositiva**: texto, texto con figura, figura grande, dos figuras y fórmula destacada, en el vídeo y en el PowerPoint (con el LaTeX y el texto alternativo en las notas).
- **Exportación a LaTeX Beamer** (`.tex` con las fórmulas en LaTeX real y las figuras en una carpeta) y figuras dentro del Word, del Markdown y del cuaderno.

Límites: las imágenes en EMF o WMF no se pueden mostrar en el navegador (guarda el documento como PDF y recórtalas); un PDF escaneado necesita OCR antes. Al analizarlas, las imágenes se envían a OpenAI tal cual, sin anonimizar.

## Novedades de la versión 2.0

- Interfaz guiada con el estilo de Forja y un apunte de ejemplo.
- **Dos puntos de partida**: mejorar un material que ya tienes (Word, PDF, PowerPoint, Markdown o cuaderno Jupyter) o **crearlo desde cero** a partir del tema, el nivel, la extensión y el enfoque.
- **Revisores**:
  - de **fidelidad**, que señala lo añadido que no estaba en el original, lo que se ha perdido y los errores introducidos, con corrección aplicable con un clic;
  - **disciplinar**, para el material creado desde cero;
  - de **preguntas**, que comprueba cada respuesta contra el material.
- **Cinco productos**:
  - el material en Word, Markdown y `.ipynb`;
  - un nanovídeo locutado con subtítulos `.srt`;
  - un **PowerPoint editable** con la narración en las notas;
  - un **banco de preguntas en formato GIFT** para Moodle;
  - un **plan de clase** presencial, en línea o de clase invertida.
- **Variantes lingüísticas**: español de España, latinoamericano neutro, rioplatense o de México, y portugués de Brasil o de Portugal, con el acento correspondiente en la voz.
- Color institucional en las diapositivas y un paquete `.zip` con todo, incluidas las órdenes de ffmpeg para montar un MP4.

## El vídeo

El navegador graba en **WebM**, que se ve en cualquier navegador y en Moodle. Para MP4, el `.zip` trae las diapositivas, los audios, los subtítulos y las órdenes de `ffmpeg`. Mientras se graba, la pestaña debe quedarse delante. Chrome, Edge y Firefox montan el vídeo; en Safari conviene la ruta del `.zip`.

## Privacidad

La clave se guarda en `localStorage` (`ia_openai_key`) y solo viaja a `api.openai.com`. Las figuras y fórmulas que analizas con IA viajan también a OpenAI, como imagen. No la uses en un ordenador compartido: el botón «Olvidarla» la borra.

## Cómo citar

Borrás Rocher, F. (2026). *NanoClase* (versión 2.1.0) [Software]. Universidad Miguel Hernández de Elche. https://doi.org/10.5281/zenodo.22300395

El DOI anterior es el de concepto: apunta siempre a la última versión. El DOI de cada versión concreta está en [Zenodo](https://doi.org/10.5281/zenodo.22300395). GitHub ofrece la cita en formato APA y BibTeX con el botón *Cite this repository*, a partir de `CITATION.cff`.

Forma parte del catálogo [Herramientas IA para la academia](https://fborrasumh.github.io/ia/).

## Licencia

MIT © 2026 Fernando Borrás Rocher · Universidad Miguel Hernández de Elche.
