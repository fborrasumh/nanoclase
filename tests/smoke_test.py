#!/usr/bin/env python3
"""Prueba de humo de NanoClase con IA simulada (sin red ni clave real).

  NODE_MODULES=/ruta/node_modules python3 tests/smoke_test.py [--lang es|en|pt|all] [--dump fichero.json] [--shots carpeta]

Sirve index.html en local, sustituye las librerías de los CDN por las de NODE_MODULES
(mammoth 1.6.0, jszip 3.10.1, pdfjs-dist 3.11.174, docx 8.5.0, pptxgenjs 3.12.0, mathjax 3.2.2)
y simula api.openai.com. Recorre el flujo completo con el apunte de ejemplo: diagnóstico, reescritura,
revisión (con una cita inventada que el código debe detectar), guion, voz, preguntas (una mal formada),
plan y paquete .zip. En inglés y portugués comprueba que no quede texto de la interfaz en español."""
import argparse, base64, functools, http.server, io, json, os, pathlib, re, struct, sys, threading, wave, zipfile
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
NM = pathlib.Path(os.environ.get('NODE_MODULES', '/home/claude/testlibs/node_modules'))
LIB = {'mammoth': 'mammoth/mammoth.browser.min.js', 'pdf.worker': 'pdfjs-dist/build/pdf.worker.min.js', 'pdf.min': 'pdfjs-dist/build/pdf.min.js',
       'jszip': 'jszip/dist/jszip.min.js', 'docx': 'docx/build/index.umd.js', 'pptxgen': 'pptxgenjs/dist/pptxgen.bundle.js', 'tex-svg': 'mathjax/es5/tex-svg.js'}

def wav(seg=1.0):
    b = io.BytesIO(); w = wave.open(b, 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(16000); w.writeframes(b'\0\0' * int(16000 * seg)); w.close(); return b.getvalue()

MD = """# Confidence intervals for a mean

## What you will learn
1. Compute a confidence interval for a mean.

## Before you start
Mean and standard deviation.

## 1. The interval
The 95% interval is

![Twenty intervals](F1)

$$ \\bar{x} \\pm t_{n-1} \\cdot \\frac{s}{\\sqrt{n}} $$ {#E1}

The ratio s/√n is the standard error of the mean. According to a 2019 study, 80% of students confuse it.

<details><summary>Show answer</summary>
128 ± 6.19.
</details>

<details><summary>Show answer</summary>
It narrows.
</details>

## Summary
- The interval narrows as n grows.

## Glossary
| Term | Definition |
|---|---|
| Standard error | s/√n |

## Common mistakes
| Mistake | Correction |
|---|---|
| Probability of this interval | Long-run frequency |

## Exercises
1. Compute the interval with n = 36.
"""
INVENTADA = 'According to a 2019 study, 80% of students confuse it.'   # cita inventada: el revisor (simulado) la señala
NO_EXISTE = 'This sentence does not appear in the rewritten material.'   # corrección sobre una cita que no está: el código no debe aplicarla

def respuesta(body):
    """IA simulada. Responde en inglés a propósito: así, en las pruebas de idioma, todo lo que quede en español es de la interfaz."""
    sis = body['messages'][0]['content'] if body.get('messages') else ''
    if isinstance(sis, list): sis = ' '.join(x.get('text', '') for x in sis)
    dims = ['objetivos', 'previos', 'estructura', 'andamiaje', 'comprobaciones', 'ejemplos', 'lenguaje', 'cierre']
    if sis.startswith('Evalúas material'):
        fin = 'What you will learn' in json.dumps(body)
        return json.dumps({'veredicto': 'Good content, little teaching design.', 'dimensiones': [{'clave': k, 'nota': (8 if fin else 4), 'comentario': 'Comment about ' + k} for k in dims],
                           'fortalezas': ['Clear clinical example'], 'carencias': ['No objectives'], 'prioridad': 'Add observable objectives'})
    if sis.startswith('Eres profesor universitario y editor') or sis.startswith('Eres profesor universitario experto en la materia'): return MD
    if sis.startswith('Eres un revisor de fidelidad'):
        return json.dumps({'veredicto': 'One statement does not come from the original.', 'anadidos': [{'gravedad': 'alta', 'texto': INVENTADA, 'comentario': 'The original cites no study.'}],
                           'omisiones': [{'texto': 'The frequentist interpretation', 'comentario': 'Summarised too much.'}],
                           'errores': [{'gravedad': 'media', 'texto': NO_EXISTE, 'comentario': 'Quote not in the text.', 'correccion': 'Another sentence.'}]})
    if sis.startswith('Eres un revisor disciplinar'): return json.dumps({'veredicto': 'No serious errors.', 'errores': []})
    if sis.startswith('Eres guionista'):
        n = int(re.search(r'de (\d+) escenas', sis).group(1))
        esc = [{'plantilla': 'texto', 'titulo': f'Scene title {i+1}', 'subtitulo': 'Subtitle', 'puntos': ['Point one', 'Point two'], 'figuras': [], 'formula': '', 'formula_hablada': '', 'narracion': 'A short narration for the scene.'} for i in range(n)]
        esc[1].update(plantilla='texto_figura', figuras=['F1', 'F9']); esc[2].update(plantilla='formula', formula='E1', formula_hablada='x bar plus or minus t')
        return json.dumps({'titulo': 'Intervals', 'escenas': esc})
    if sis.startswith('Eres experto en evaluación universitaria'):
        return json.dumps({'preguntas': [
            {'tipo': 'mc', 'enunciado': 'What does the standard error measure?', 'opciones': ['The precision of the mean', 'The spread of the data', 'The sample size', 'The confidence level'], 'correcta': 0, 'nivel': 'recordar', 'seccion': '1', 'retro': 'It measures the precision of the mean.'},
            {'tipo': 'vf', 'enunciado': 'The interval narrows as n grows.', 'respuesta': True, 'nivel': 'recordar', 'seccion': '1', 'retro': 'The standard error falls.'},
            {'tipo': 'mc', 'enunciado': 'Which one is right?', 'opciones': ['A', 'A'], 'correcta': 5, 'nivel': 'aplicar', 'seccion': '1', 'retro': ''},
            {'tipo': 'corta', 'enunciado': 'How many degrees of freedom are there with n = 25?', 'respuesta': ['24'], 'nivel': 'aplicar', 'seccion': '1', 'retro': 'n − 1.'}]})
    if sis.startswith('Eres revisor de bancos'): return json.dumps({'revision': [{'id': 1, 'estado': 'ok'}, {'id': 2, 'estado': 'ok'}, {'id': 3, 'estado': 'descartar', 'motivo': 'Repeated options.'}, {'id': 4, 'estado': 'ok'}]})
    if sis.startswith('Eres profesor universitario experto en metodologías'): return '# Session\n\n| Minute | Activity |\n|---|---|\n| 0-90 | Practice |\n'
    if sis.startswith('Miras una figura'): return json.dumps({'clase': 'gráfica', 'pie': 'A chart', 'alt': 'A test chart.', 'relevante': True})
    if sis.startswith('Transcribes a LaTeX'): return json.dumps({'latex': 'x^2', 'hablada': 'x squared', 'confianza': 'media', 'nota': 'Blurry.'})
    if sis.startswith('Comparas dos imágenes'): return json.dumps({'coincide': False, 'diferencias': 'A subscript is missing.', 'latex': 'x_1^2'})
    return json.dumps({'ok': True})

def instala_rutas(page, log):
    def lib(route):
        u = route.request.url
        for k, f in LIB.items():
            if k in u: return route.fulfill(path=str(NM / f), content_type='application/javascript')
        return route.fulfill(status=404, body='')
    page.route(re.compile(r'https://(cdnjs\.cloudflare\.com|cdn\.jsdelivr\.net)/.*'), lib)
    page.route(re.compile(r'https://fonts\.(googleapis|gstatic)\.com/.*'), lambda r: r.fulfill(status=200, body='', content_type='text/css'))
    def api(route):
        req = route.request; u = req.url
        if u.endswith('/models'): return route.fulfill(json={'data': [{'id': x} for x in ['gpt-6-luna', 'gpt-4.1-mini', 'gpt-4o', 'tts-1', 'whisper-1', 'text-embedding-3-small']]})
        if '/audio/speech' in u: return route.fulfill(body=wav(1.2), content_type='audio/wav')
        body = json.loads(req.post_data or '{}'); txt = respuesta(body); log.append(body)
        if body.get('stream'):
            sse = ''.join('data: ' + json.dumps({'choices': [{'delta': {'content': txt[i:i + 400]}}]}) + '\n\n' for i in range(0, len(txt), 400)) + 'data: [DONE]\n\n'
            return route.fulfill(body=sse, content_type='text/event-stream')
        return route.fulfill(json={'choices': [{'message': {'content': txt}}]})
    page.route(re.compile(r'https://api\.openai\.com/.*'), api)

def servidor():
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT))
    class Q(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    s = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Q, directory=str(ROOT)))
    threading.Thread(target=s.serve_forever, daemon=True).start(); return s

RECOGE = """() => {
  const out = {txt: new Set(), attr: new Set(), html: new Set()};
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for(let n = w.nextNode(); n; n = w.nextNode()){ const p = n.parentElement; if(!p || _skip(p)) continue;
    if(p.id === 'registro'){ n.data.split('\\n').forEach(l => { l = _norm(l); if(/[a-záéíóúñ]{3}/i.test(l)) out.txt.add(l); }); continue; }
    const s = _norm(n.data); if(/[a-záéíóúñ]{2}/i.test(s)) out.txt.add(s); }
  document.querySelectorAll('*').forEach(el => { if(_skip(el)) return; ['placeholder','title','aria-label','alt'].forEach(a => { const v = el.getAttribute(a); if(v && /[a-záéíóúñ]{3}/i.test(v)) out.attr.add(_norm(v)); });
    if(el.children.length && _frase(el) && !(el.parentElement && _frase(el.parentElement))) out.html.add(_norm(el.innerHTML)); });
  return {txt: [...out.txt], attr: [...out.attr], html: [...out.html]};
}"""

def flujo(page, lang, fallos, recoge=None, shots=None):
    """Recorre la app completa. Devuelve lo recogido (textos) si recoge."""
    bag = {'txt': set(), 'attr': set(), 'html': set()}
    def mira(nombre):
        if recoge:
            r = page.evaluate(RECOGE); [bag[k].update(r[k]) for k in bag]
        if lang != 'es':
            f = page.evaluate('i18nFaltan()')
            for x in f: fallos.add(f'[{lang}] {nombre}: {x}')
        if shots: page.screenshot(path=f'{shots}/{lang}_{nombre}.png', full_page=False)
    page.wait_for_timeout(300); mira('portada')
    page.click('#btnHelp'); page.wait_for_timeout(150); mira('ayuda'); page.click('#mHelp [data-close]')
    page.click('#btnEj'); page.wait_for_timeout(600); mira('partida')
    assert page.locator('#galeria [data-id]').count() == 2, 'el ejemplo debe traer una figura y una fórmula'
    nota = page.inner_text('#notaDoc')
    if lang == 'en': assert 'Example notes' in nota, nota
    # modo crear (sin clave: solo la pantalla)
    page.click('[data-modo="crear"]'); page.wait_for_timeout(150); mira('crear'); page.click('[data-modo="mejorar"]')
    page.click('#stepper [data-go="1"]'); page.wait_for_timeout(200); mira('ajustes_sin_clave')
    page.fill('#clave', 'sk-test-0000000000000000000000'); page.wait_for_timeout(1300)
    opts = page.eval_on_selector_all('#selModeloTexto option', 'o => o.map(x => x.value)')
    assert 'gpt-4.1-mini' in opts and 'tts-1' not in opts and '__otro' in opts, opts
    page.click('#btnTest'); page.wait_for_timeout(400); mira('ajustes')
    page.select_option('#selModeloTexto', '__otro'); assert page.is_visible('#modeloTexto'); page.fill('#modeloTexto', 'gpt-4.1-mini'); page.dispatch_event('#modeloTexto', 'change')
    assert page.input_value('#modeloTexto') == 'gpt-4.1-mini'; page.select_option('#selModeloTexto', 'gpt-6-luna')
    page.click('#stepper [data-go="2"]'); page.wait_for_timeout(200)
    page.click('#btnAnalizar') if page.is_enabled('#btnAnalizar') else None
    page.wait_for_timeout(300)
    if page.is_enabled('#btnVerificar'): page.click('#btnVerificar'); page.wait_for_timeout(1500)
    mira('galeria')
    # recorte
    page.click('#btnRecortar'); page.wait_for_timeout(500); mira('recorte'); page.click('#mRecorte [data-close]')
    page.once('dialog', lambda d: d.accept())
    page.click('#navNext'); page.wait_for_timeout(1500); mira('diagnostico')
    assert page.locator('#evalInicial table.rubrica').count() == 1
    page.click('#navNext'); page.wait_for_timeout(3000); mira('material')
    qa = page.inner_text('#qa')
    assert INVENTADA[:30] in qa, 'el revisor debe señalar la cita inventada'
    # la corrección de una cita que no está en el texto no se aplica
    page.locator('#qa [data-fix]').first.dispatch_event('click'); page.wait_for_timeout(200)
    assert NO_EXISTE not in page.input_value('#mejorado')
    page.click('#matTabs [data-mt="editar"]'); page.wait_for_timeout(100); page.click('#matTabs [data-mt="ver"]')
    page.click('#navNext'); page.wait_for_timeout(300); mira('productos')
    page.click('#btnGuion'); page.wait_for_timeout(3000); mira('guion')
    av = page.inner_text('#avisoRecursos'); assert 'F9' in av, 'el código debe quitar la figura inexistente F9'
    page.click('#tabJson'); page.wait_for_timeout(100); page.fill('#jsonGuion', '{"escenas":[]}'); page.click('#btnAplicarJson'); page.wait_for_timeout(200); mira('json_malo'); page.click('#btnRevertirJson'); page.click('#tabFichas')
    page.click('#btnVoz'); page.wait_for_timeout(4000); mira('voz')
    page.click('#ptabs [data-p="preg"]'); page.click('#btnPreg'); page.wait_for_timeout(2000); mira('preguntas')
    assert page.locator('#pregList .preg.descartada').count() == 1, 'la pregunta mal formada debe quedar descartada'
    page.click('#ptabs [data-p="plan"]'); page.click('#btnPlan'); page.wait_for_timeout(1500); mira('plan')
    page.click('#ptabs [data-p="pack"]'); page.wait_for_timeout(200); mira('paquete')
    with page.expect_download(timeout=60000) as d: page.click('#btnDescargarZip')
    z = zipfile.ZipFile(d.value.path()); nombres = z.namelist()
    for f in ['guion.json', 'subtitulos.srt', 'preguntas/banco_moodle.gift.txt', 'plan_de_clase/plan.md']: assert f in nombres, (f, nombres)
    assert any(n.endswith('.docx') for n in nombres) and any(n.endswith('.pptx') for n in nombres), nombres
    page.click('#ptabs [data-p="preg"]')
    with page.expect_download() as d: page.click('#btnGift')
    assert 'Which one is right?' not in pathlib.Path(d.value.path()).read_text(), 'la pregunta descartada no debe ir al GIFT'
    return bag

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--lang', default='all'); ap.add_argument('--dump'); ap.add_argument('--shots'); ap.add_argument('--movil', action='store_true')
    a = ap.parse_args(); s = servidor(); url = f'http://127.0.0.1:{s.server_port}/index.html'
    langs = ['es', 'en', 'pt'] if a.lang == 'all' else [a.lang]; fallos = set(); bag = {'txt': set(), 'attr': set(), 'html': set()}
    if a.shots: pathlib.Path(a.shots).mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
        for lang in langs:
            ctx = b.new_context(accept_downloads=True, **({'viewport': {'width': 390, 'height': 844}, 'device_scale_factor': 1, 'is_mobile': True, 'has_touch': True} if a.movil else {'viewport': {'width': 1280, 'height': 900}}))
            page = ctx.new_page(); errs = []; log = []
            page.on('pageerror', lambda e: errs.append(str(e))); page.on('console', lambda m: errs.append(m.text) if m.type == 'error' and 'Failed to load resource' not in m.text else None)
            instala_rutas(page, log)
            page.goto(url + ('' if lang == 'es' else f'?lang={lang}')); page.wait_for_timeout(500)
            assert page.evaluate('LANG') == lang
            r = flujo(page, lang, fallos, recoge=bool(a.dump), shots=a.shots)
            [bag[k].update(r[k]) for k in bag]
            if a.movil:
                ancho = page.evaluate('document.documentElement.scrollWidth'); assert ancho <= 392, f'desborde horizontal en móvil: {ancho}px'
            # el idioma persiste al recargar
            page.goto(url); page.wait_for_timeout(400); assert page.evaluate('LANG') == lang, 'el idioma no persiste'
            if lang != 'es':
                page.select_option('#selLang', 'es'); page.wait_for_timeout(200)
                assert 'De un tema o un apunte' in page.inner_text('.hero h1'), 'no vuelve al español'
            if errs: fallos.update(f'[{lang}] consola: {e}' for e in errs)
            print(f'✓ {lang}: flujo completo · {len(log)} llamadas a la IA simulada')
            ctx.close()
        b.close()
    if a.dump: pathlib.Path(a.dump).write_text(json.dumps({k: sorted(v) for k, v in bag.items()}, ensure_ascii=False, indent=1))
    if fallos:
        print(f'✗ {len(fallos)} problemas:'); [print('  ', f) for f in sorted(fallos)]; sys.exit(1)
    print('✓ sin textos sin traducir ni errores de consola')

if __name__ == '__main__':
    main()
