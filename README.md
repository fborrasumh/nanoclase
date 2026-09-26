# NanoClase

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22300395.svg)](https://doi.org/10.5281/zenodo.22300395)

**Aplicación:** https://fborrasumh.github.io/nanoclase/

Crea o mejora un **material docente** y genera, a partir de él, todo lo que necesita una clase universitaria. Está pensada para el profesorado universitario iberoamericano. Aplicación de un solo fichero, sin servidor: todo ocurre en el navegador con tu clave de OpenAI.

## Novedades de la versión 2.0

- Interfaz guiada con el estilo de Forja y un apunte de ejemplo.
- **Dos puntos de partida**: mejorar un material que ya tienes (Word, PDF, Markdown o cuaderno Jupyter) o **crearlo desde cero** a partir del tema, el nivel, la extensión y el enfoque.
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

La clave se guarda en `localStorage` (`ia_openai_key`) y solo viaja a `api.openai.com`. No la uses en un ordenador compartido: el botón «Olvidarla» la borra.

## Cómo citar

Borrás Rocher, F. (2026). *NanoClase* (versión 2.0.0) [Software]. Universidad Miguel Hernández de Elche. https://doi.org/10.5281/zenodo.22300395

El DOI anterior es el de concepto: apunta siempre a la última versión. El DOI de cada versión concreta está en [Zenodo](https://doi.org/10.5281/zenodo.22300395). GitHub ofrece la cita en formato APA y BibTeX con el botón *Cite this repository*, a partir de `CITATION.cff`.

Forma parte del catálogo [Herramientas IA para la academia](https://fborrasumh.github.io/ia/).

## Licencia

MIT © 2026 Fernando Borrás Rocher · Universidad Miguel Hernández de Elche.
