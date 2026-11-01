#!/usr/bin/env python3
"""Generate the project case-study pages (ES + EN) from the content below.

Output:  /proyectos/<slug>/index.html  and  /en/projects/<slug>/index.html
Usage:   python3 tools/build_cases.py
"""

import html
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
BASE = "https://juanjrp.github.io"

# Eval loss of the published LoRA adapter (trainer_state.json of llm-finetuning, checkpoint-1686).
LLM_LOSS = [(100, 3.041), (200, 2.952), (300, 2.915), (400, 2.892), (500, 2.872), (600, 2.858), (700, 2.846),
            (800, 2.836), (900, 2.828), (1000, 2.820), (1100, 2.815), (1200, 2.810), (1300, 2.806),
            (1400, 2.804), (1500, 2.802), (1600, 2.801)]


def loss_chart(lang: str) -> str:
    """Small inline SVG line chart; colours come from the site's CSS tokens so it follows the theme."""
    w, h, pl, pr, pt, pb = 640, 240, 48, 16, 16, 36
    xs = [s for s, _ in LLM_LOSS]; ys = [v for _, v in LLM_LOSS]
    x0, x1, y0, y1 = 0, 1700, 2.78, 3.06
    X = lambda s: pl + (s - x0) / (x1 - x0) * (w - pl - pr)
    Y = lambda v: pt + (y1 - v) / (y1 - y0) * (h - pt - pb)
    pts = " ".join(f"{X(s):.1f},{Y(v):.1f}" for s, v in LLM_LOSS)
    grid = "".join(
        f'<line x1="{pl}" x2="{w - pr}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" class="g"/>'
        f'<text x="{pl - 8}" y="{Y(v) + 4:.1f}" text-anchor="end">{v:.2f}</text>' for v in (2.8, 2.9, 3.0))
    xt = "".join(f'<text x="{X(s):.1f}" y="{h - 12}" text-anchor="middle">{s}</text>' for s in (100, 400, 800, 1200))
    dots = "".join(f'<circle cx="{X(s):.1f}" cy="{Y(v):.1f}" r="2.6"/>' for s, v in LLM_LOSS)
    label = "Pérdida de evaluación por paso de entrenamiento" if lang == "es" else "Evaluation loss per training step"
    step = "paso" if lang == "es" else "step"
    return (f'<figure class="case-fig"><svg class="chart" viewBox="0 0 {w} {h}" role="img" aria-label="{label}: de 3.041 a 2.801">'
            f'{grid}{xt}<polyline points="{pts}"/>{dots}'
            f'<text x="{w - pr}" y="{h - 12}" text-anchor="end" class="u">{step}</text></svg>'
            f'<figcaption>{label}. ' + ("Mejor checkpoint: paso 1600 (2.801)." if lang == "es" else "Best checkpoint: step 1600 (2.801).")
            + "</figcaption></figure>")


CASES = [
    {
        "slug": "cyber-vanish", "repo": "cyber-vanish",
        "stack": ["Python", "MediaPipe", "OpenCV", "NumPy", "pytest", "GitHub Actions"],
        "es": {
            "kind": "visión por computador · tiempo real",
            "title": "Cyber Vanish",
            "lead": "Chasqueas los dedos y desapareces de la videollamada. Detecta el gesto y el sonido en tiempo real, "
                    "te borra del video con uno de 14 efectos y envía el resultado a una cámara virtual que funciona en "
                    "Meet, Zoom, Teams u OBS.",
            "facts": [("14", "efectos de desintegración"), ("6–25 ms", "por frame a 1280×720"), ("2", "señales para el chasquido: imagen + audio")],
            "media": '<figure class="case-fig"><img src="/assets/images/cases/cyber-vanish.webp" width="360" height="360" alt="Los efectos cyber, polvo, fuego y matrix desintegrando a una persona" loading="lazy"><figcaption>Cuatro de los efectos aplicados con el código real del proyecto.</figcaption></figure>',
            "sections": [
                ("El reto", "<p>Hacer desaparecer a una persona de un video en vivo exige tres cosas a la vez: saber qué píxeles son "
                 "la persona, saber qué había detrás de ella y dibujar la transición sin que la llamada se trabe. Todo en la "
                 "CPU de un portátil, a 30 cuadros por segundo.</p>"),
                ("Cómo funciona", '<pre class="case-diagram">webcam ─► MediaPipe (segmentación + mano) ─┐\n'
                 'micrófono ─► detector de chasquido (audio) ──┼─► ¿chasquido? ─► efecto (14) ─► cámara virtual\n'
                 '             fondo capturado o aprendido ──┘                       └─► vista previa</pre>'
                 "<ul><li><b>Disparo robusto:</b> el chasquido se confirma con la cámara (pulgar y dedo corazón juntos) y "
                 "con el micrófono (sonido seco) a la vez, para no activarse con cualquier ruido.</li>"
                 "<li><b>Fondo:</b> se captura la habitación vacía o se aprende mientras te mueves. Lo que nunca se vio se "
                 "reconstruye copiando textura real de la habitación (completado por ejemplos), no estirando bordes.</li>"
                 "<li><b>Efectos como plugins:</b> cada efecto es una clase que hereda de <code>Vanish</code> y se registra "
                 "con un decorador; la base maneja estados, fondo, partículas y física.</li></ul>"),
                ("Decisiones técnicas", "<ul><li>Probé <b>LaMa</b> (una red neuronal de <i>inpainting</i>) para rellenar el fondo: "
                 "con huecos del tamaño de una persona dejaba una sombra con su forma, tardaba 3–4 s en CPU y pesaba 208 MB. "
                 "La descarté por un método clásico que da mejor resultado aquí.</li>"
                 "<li>El relleno lento (~2 s) corre en segundo plano y mientras tanto se usa uno rápido, para no frenar el video.</li>"
                 "<li>Las partes difuminadas (llamas, humo, halos) se calculan a 1/4 de resolución para mantener cada frame por debajo de 25 ms.</li></ul>"),
                ("Calidad", "<p>Cada efecto tiene pruebas automáticas que recorren el ciclo completo (desaparecer → invisible → "
                 "aparecer) y verifican que no quede rastro de la persona. Corren en GitHub Actions con Python 3.10 y 3.12.</p>"),
            ],
        },
        "en": {
            "kind": "computer vision · real time",
            "title": "Cyber Vanish",
            "lead": "Snap your fingers and vanish from the video call. It detects the gesture and the sound in real time, "
                    "erases you from the video with one of 14 effects and sends the result to a virtual camera that works "
                    "in Meet, Zoom, Teams or OBS.",
            "facts": [("14", "disintegration effects"), ("6–25 ms", "per frame at 1280×720"), ("2", "signals for the snap: image + audio")],
            "media": '<figure class="case-fig"><img src="/assets/images/cases/cyber-vanish.webp" width="360" height="360" alt="The cyber, dust, fire and matrix effects disintegrating a person" loading="lazy"><figcaption>Four of the effects, rendered with the project\'s actual code.</figcaption></figure>',
            "sections": [
                ("The challenge", "<p>Making a person disappear from live video takes three things at once: knowing which pixels are "
                 "the person, knowing what was behind them, and drawing the transition without freezing the call. All on a "
                 "laptop CPU, at 30 frames per second.</p>"),
                ("How it works", '<pre class="case-diagram">webcam ─► MediaPipe (segmentation + hand) ─┐\n'
                 'microphone ─► snap detector (audio) ───────┼─► snap? ─► effect (14) ─► virtual camera\n'
                 '         captured or learned background ──┘                    └─► preview</pre>'
                 "<ul><li><b>Robust trigger:</b> the snap is confirmed by the camera (thumb and middle finger together) and "
                 "the microphone (a sharp sound) at the same time, so random noise doesn't fire it.</li>"
                 "<li><b>Background:</b> captured from the empty room or learned as you move. What was never seen is rebuilt by "
                 "copying real room texture (exemplar-based completion), not by stretching edges.</li>"
                 "<li><b>Effects as plugins:</b> each effect is a class that inherits from <code>Vanish</code> and registers "
                 "itself with a decorator; the base handles states, background, particles and physics.</li></ul>"),
                ("Technical decisions", "<ul><li>I tried <b>LaMa</b> (an inpainting neural network) to fill the background: with "
                 "person-sized holes it left a person-shaped shadow, took 3–4 s on CPU and weighed 208 MB. I dropped it for a "
                 "classical method that works better here.</li>"
                 "<li>The slow fill (~2 s) runs in the background while a fast one is used, so the video never stalls.</li>"
                 "<li>Blurry layers (flames, smoke, glows) are computed at 1/4 resolution to keep every frame under 25 ms.</li></ul>"),
                ("Quality", "<p>Every effect has automated tests that run the full cycle (vanish → invisible → reappear) and check "
                 "that no trace of the person is left. They run on GitHub Actions with Python 3.10 and 3.12.</p>"),
            ],
        },
    },
    {
        "slug": "nyc-taxi-pipeline", "repo": "nyc-taxi-pipeline",
        "stack": ["PySpark", "Parquet", "MongoDB", "Docker", "matplotlib", "GitHub Actions"],
        "es": {
            "kind": "ingeniería de datos · batch",
            "title": "NYC Taxi Pipeline",
            "lead": "Un pipeline de datos de punta a punta sobre los viajes reales de los taxis amarillos de Nueva York: "
                    "descarga los datos públicos, los limpia y agrega con Spark, los guarda en Parquet y MongoDB y produce "
                    "un tablero ejecutivo. Todo se levanta con un solo comando de Docker.",
            "facts": [("~12", "archivos Parquet por año (50–100 MB c/u)"), ("8", "reglas de limpieza"), ("6", "gráficas, incluido un tablero ejecutivo")],
            "media": '<figure class="case-fig"><img src="/assets/images/cases/nyc-dashboard.webp" width="1400" height="791" alt="Tablero ejecutivo con demanda, ingresos, zonas y métodos de pago" loading="lazy"><figcaption>Tablero ejecutivo generado al final del pipeline.</figcaption></figure>',
            "sections": [
                ("El problema", "<p>La comisión de taxis de Nueva York (TLC) necesita entender la demanda, la rentabilidad y la "
                 "operación del servicio: en qué horas y zonas se concentran los viajes, cómo evolucionan los ingresos y cómo pagan "
                 "los pasajeros. Los datos existen, pero son millones de registros mensuales con errores.</p>"),
                ("Arquitectura", '<pre class="case-diagram">TLC (Parquet mensual) ─► ingesta.py ─► PySpark ─┬─► Parquet particionado (año/mes)\n'
                 '                                                ├─► MongoDB (agregados)\n'
                 '                                                └─► 6 gráficas + tablero</pre>'
                 "<p>Cada etapa es un script independiente y <code>run_pipeline.py</code> las orquesta. Docker Compose levanta "
                 "Spark y MongoDB, así que cualquiera lo reproduce igual.</p>"),
                ("Decisiones técnicas", "<ul><li><b>Batch, no streaming:</b> la TLC publica datos históricos mensuales, no un flujo "
                 "en tiempo real, y el batch da resultados idénticos en cada ejecución. Si hubiera GPS en vivo, la ingesta se "
                 "cambiaría por Kafka + Spark Structured Streaming sin tocar el resto.</li>"
                 "<li><b>Calidad de datos:</b> se descartan tarifas fuera de $2.50–$500, distancias fuera de 0.1–100 millas, "
                 "pasajeros fuera de 1–6, viajes de más de 4 horas, propinas negativas y viajes que terminan antes de empezar.</li>"
                 "<li><b>Parquet + MongoDB:</b> Parquet para el detalle (columnar y particionado) y MongoDB para los agregados que "
                 "consultan las gráficas.</li></ul>"),
                ("Resultado", '<figure class="case-fig"><img src="/assets/images/cases/nyc-heatmap.webp" width="1100" height="425" alt="Mapa de calor de demanda por hora y día de la semana" loading="lazy"><figcaption>Demanda por hora y día de la semana.</figcaption></figure>'
                 "<p>El pipeline responde las preguntas de negocio con agregados por hora, día, mes, zona y método de pago. El CI "
                 "verifica el código y construye la imagen de Docker en cada cambio.</p>"),
            ],
        },
        "en": {
            "kind": "data engineering · batch",
            "title": "NYC Taxi Pipeline",
            "lead": "An end-to-end data pipeline over real New York yellow-cab trips: it downloads the public data, cleans and "
                    "aggregates it with Spark, stores it in Parquet and MongoDB and produces an executive dashboard. One Docker "
                    "command runs it all.",
            "facts": [("~12", "Parquet files per year (50–100 MB each)"), ("8", "data-quality rules"), ("6", "charts, including an executive dashboard")],
            "media": '<figure class="case-fig"><img src="/assets/images/cases/nyc-dashboard.webp" width="1400" height="791" alt="Executive dashboard with demand, revenue, zones and payment methods" loading="lazy"><figcaption>Executive dashboard produced at the end of the pipeline.</figcaption></figure>',
            "sections": [
                ("The problem", "<p>New York's Taxi &amp; Limousine Commission (TLC) needs to understand demand, profitability and "
                 "operations: which hours and zones concentrate trips, how revenue evolves and how passengers pay. The data "
                 "exists, but it's millions of monthly records with errors.</p>"),
                ("Architecture", '<pre class="case-diagram">TLC (monthly Parquet) ─► ingesta.py ─► PySpark ─┬─► partitioned Parquet (year/month)\n'
                 '                                                ├─► MongoDB (aggregates)\n'
                 '                                                └─► 6 charts + dashboard</pre>'
                 "<p>Each stage is an independent script orchestrated by <code>run_pipeline.py</code>. Docker Compose brings up "
                 "Spark and MongoDB, so anyone can reproduce it exactly.</p>"),
                ("Technical decisions", "<ul><li><b>Batch, not streaming:</b> the TLC publishes monthly historical data, not a "
                 "live feed, and batch gives identical results on every run. With live GPS data, ingestion could be swapped for "
                 "Kafka + Spark Structured Streaming without touching the rest.</li>"
                 "<li><b>Data quality:</b> drops fares outside $2.50–$500, distances outside 0.1–100 miles, passenger counts "
                 "outside 1–6, trips over 4 hours, negative tips and trips that end before they start.</li>"
                 "<li><b>Parquet + MongoDB:</b> Parquet for the detail (columnar, partitioned) and MongoDB for the aggregates "
                 "the charts query.</li></ul>"),
                ("Result", '<figure class="case-fig"><img src="/assets/images/cases/nyc-heatmap.webp" width="1100" height="425" alt="Demand heatmap by hour and weekday" loading="lazy"><figcaption>Demand by hour and day of the week.</figcaption></figure>'
                 "<p>The pipeline answers the business questions with aggregates by hour, day, month, zone and payment method. "
                 "CI checks the code and builds the Docker image on every change.</p>"),
            ],
        },
    },
    {
        "slug": "llm-finetuning", "repo": "llm-finetuning",
        "stack": ["PyTorch", "Hugging Face", "PEFT / QLoRA", "bitsandbytes", "python-telegram-bot"],
        "es": {
            "kind": "ia generativa · fine-tuning",
            "title": "Fine-tuning de un LLM",
            "lead": "Ajusté DeepSeek-R1 (1.5B parámetros) para que responda en español preguntas prácticas tipo «¿cómo hago…?», "
                    "entrenándolo con QLoRA en una sola GPU, y lo puse a conversar por un bot de Telegram. Proyecto hecho en "
                    "pareja en la universidad.",
            "facts": [("~106 mil", "pares pregunta/respuesta en español"), ("4 bits", "cuantización para caber en una GPU"), ("3.04 → 2.80", "pérdida de evaluación")],
            "media": None,
            "sections": [
                ("Método", "<ul><li><b>Datos:</b> ~152 mil pares en formato chat; entrené con 106 mil (90 % entrenamiento, 10 % evaluación).</li>"
                 "<li><b>QLoRA:</b> el modelo base se carga cuantizado a 4 bits (NF4) y solo se entrenan adaptadores LoRA pequeños "
                 "(<code>r=8</code>), así el entrenamiento cabe en una GPU de consumo.</li>"
                 "<li><b>Entrenamiento:</b> 3 épocas, lote efectivo de 32, <i>gradient checkpointing</i> y fp16; se guarda el mejor "
                 "checkpoint según la pérdida de evaluación.</li>"
                 "<li><b>Servicio:</b> un bot de Telegram carga el modelo base + el adaptador, aplica la plantilla de chat y limpia "
                 "el bloque de razonamiento <code>&lt;think&gt;</code> antes de responder.</li></ul>"),
                ("Resultados", "__CHART__<p>La pérdida baja de forma constante y se estabiliza al final de la tercera época, sin "
                 "señales de sobreajuste.</p>"),
                ("Lo que aprendí", "<p>Al documentar el proyecto encontré dos erratas en las capas donde se aplica LoRA "
                 "(<code>\"k,proj\"</code> y <code>\"0_proj\"</code>). PEFT las ignora sin avisar, así que el adaptador publicado "
                 "solo se entrenó sobre dos de las cuatro proyecciones de atención. Lo corregí en el código y lo dejé documentado: "
                 "reentrenar con las cuatro debería mejorar el resultado. La lección: <b>verificar los parámetros entrenables</b> "
                 "(<code>print_trainable_parameters</code>) contra lo que esperas antes de gastar horas de GPU.</p>"),
            ],
        },
        "en": {
            "kind": "generative ai · fine-tuning",
            "title": "LLM fine-tuning",
            "lead": "I fine-tuned DeepSeek-R1 (1.5B parameters) to answer practical \"how do I…?\" questions in Spanish, training it "
                    "with QLoRA on a single GPU, and served it through a Telegram bot. A two-person university project.",
            "facts": [("~106K", "Spanish Q&amp;A pairs"), ("4-bit", "quantization to fit one GPU"), ("3.04 → 2.80", "evaluation loss")],
            "media": None,
            "sections": [
                ("Method", "<ul><li><b>Data:</b> ~152K pairs in chat format; trained on 106K (90% train, 10% eval).</li>"
                 "<li><b>QLoRA:</b> the base model is loaded 4-bit quantized (NF4) and only small LoRA adapters are trained "
                 "(<code>r=8</code>), so training fits a consumer GPU.</li>"
                 "<li><b>Training:</b> 3 epochs, effective batch size 32, gradient checkpointing and fp16; the best checkpoint by "
                 "eval loss is kept.</li>"
                 "<li><b>Serving:</b> a Telegram bot loads the base model + adapter, applies the chat template and strips the "
                 "<code>&lt;think&gt;</code> reasoning block before replying.</li></ul>"),
                ("Results", "__CHART__<p>Loss drops steadily and levels off by the end of the third epoch, with no sign of overfitting.</p>"),
                ("What I learned", "<p>While documenting the project I found two typos in the layers LoRA targets "
                 "(<code>\"k,proj\"</code> and <code>\"0_proj\"</code>). PEFT silently ignores them, so the published adapter was "
                 "only trained on two of the four attention projections. I fixed the code and documented it: retraining on all four "
                 "should improve the result. The lesson: <b>check the trainable parameters</b> (<code>print_trainable_parameters</code>) "
                 "against what you expect before burning GPU hours.</p>"),
            ],
        },
    },
]

UI = {
    "es": {"home": "/", "back": "← volver a proyectos", "anchor": "/#proyectos", "code": "Ver el código en GitHub",
           "stack": "Stack", "other": "Otros casos", "lang_href": "/en/projects/{slug}/", "lang_label": "EN",
           "lang_title": "Read in English", "skip": "Saltar al contenido", "theme": "Cambiar tema claro/oscuro",
           "site": "código del sitio", "path": "/proyectos/{slug}/", "locale": "es_CO", "case": "caso de estudio"},
    "en": {"home": "/en/", "back": "← back to projects", "anchor": "/en/#projects", "code": "View the code on GitHub",
           "stack": "Stack", "other": "More case studies", "lang_href": "/proyectos/{slug}/", "lang_label": "ES",
           "lang_title": "Leer en español", "skip": "Skip to content", "theme": "Toggle light/dark theme",
           "site": "site source", "path": "/en/projects/{slug}/", "locale": "en_US", "case": "case study"},
}

ICONS = """<svg class="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>
          <svg class="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>"""


def page(case: dict, lang: str) -> str:
    c, u, slug = case[lang], UI[lang], case["slug"]
    url = BASE + u["path"].format(slug=slug)
    other_lang = "en" if lang == "es" else "es"
    alt_url = BASE + UI[other_lang]["path"].format(slug=slug)
    lead_plain = html.unescape(c["lead"])
    facts = "".join(f'<div class="fact"><dt>{n}</dt><dd>{t}</dd></div>' for n, t in c["facts"])
    sections = "".join(f"<section><h2>{h}</h2>{body.replace('__CHART__', loss_chart(lang))}</section>" for h, body in c["sections"])
    others = "".join(
        f'<li><a href="{UI[lang]["path"].format(slug=o["slug"])}">{o[lang]["title"]}</a> <span>{o[lang]["kind"]}</span></li>'
        for o in CASES if o["slug"] != slug)
    tags = "".join(f"<li>{t}</li>" for t in case["stack"])
    return f"""<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{c['title']} · {u['case']} · Juan José Restrepo</title>
  <meta name="description" content="{html.escape(lead_plain)}">
  <meta name="author" content="Juan José Restrepo Pabón">
  <meta name="theme-color" content="#fafaf8" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#0b0f14" media="(prefers-color-scheme: dark)">
  <link rel="canonical" href="{url}">
  <link rel="alternate" hreflang="{lang}" href="{url}">
  <link rel="alternate" hreflang="{other_lang}" href="{alt_url}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{c['title']} · {u['case']}">
  <meta property="og:description" content="{html.escape(lead_plain)}">
  <meta property="og:image" content="{BASE}/assets/images/og.png">
  <meta property="og:locale" content="{u['locale']}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/css/main.css">
  <script>document.documentElement.classList.add("js");try{{var t=localStorage.getItem("theme");if(t)document.documentElement.dataset.theme=t}}catch(e){{}}</script>
</head>
<body>
  <a class="skip-link" href="#main">{u['skip']}</a>
  <header class="site-header">
    <div class="wrap">
      <a class="brand" href="{u['home']}">juan<span>@</span>restrepo</a>
      <nav class="nav" aria-label="{'Principal' if lang == 'es' else 'Main'}">
        <a class="nav-tool" href="{UI[lang]['lang_href'].format(slug=slug)}" hreflang="{other_lang}" lang="{other_lang}" title="{u['lang_title']}">{u['lang_label']}</a>
        <button class="nav-tool theme-toggle" type="button" data-theme-toggle aria-label="{u['theme']}">
          {ICONS}
        </button>
      </nav>
    </div>
  </header>
  <main id="main" class="case">
    <div class="wrap case-wrap">
      <a class="case-back" href="{u['anchor']}">{u['back']}</a>
      <p class="case-kind">{c['kind']}</p>
      <h1>{c['title']}</h1>
      <p class="case-lead">{c['lead']}</p>
      <div class="case-actions">
        <a class="btn btn-primary" href="https://github.com/JuanJRP/{case['repo']}">{u['code']}</a>
      </div>
      <dl class="facts wins case-facts">{facts}</dl>
      {c['media'] or ''}
      {sections}
      <section><h2>{u['stack']}</h2><ul class="tags">{tags}</ul></section>
      <nav class="case-more" aria-label="{u['other']}"><h2>{u['other']}</h2><ul>{others}</ul></nav>
    </div>
  </main>
  <footer class="site-footer">
    <div class="wrap">
      <span>© <span data-year>2026</span> Juan José Restrepo Pabón</span>
      <a href="https://github.com/JuanJRP/juanjrp.github.io">{u['site']}</a>
    </div>
  </footer>
  <script src="/assets/js/main.js" defer></script>
</body>
</html>
"""


def main() -> None:
    for case in CASES:
        for lang in ("es", "en"):
            out = SITE / UI[lang]["path"].format(slug=case["slug"]).strip("/") / "index.html"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(page(case, lang), encoding="utf-8")
            print("built", out.relative_to(SITE))


if __name__ == "__main__":
    main()
