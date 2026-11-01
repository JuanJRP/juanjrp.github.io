# juanjrp.github.io

Personal site of Juan José Restrepo — <https://juanjrp.github.io>

Plain HTML, CSS and vanilla JavaScript. No build step, no framework.

- Typing terminal, rotating role, scroll reveals and timeline progress (all disabled with `prefers-reduced-motion`)
- Project filters and cursor spotlight on cards
- Contact form delivered by [FormSubmit](https://formsubmit.co) (no backend needed)

```
index.html          Spanish (default)
en/index.html       English
assets/css/main.css Design tokens, light/dark themes, layout
assets/js/main.js   Theme, motion, filters, contact form
assets/images/      Portrait and social preview (og.png)
assets/docs/        Résumé PDFs (es/ and en/), generated from ../cv/build.py
```

Run locally:

```bash
python3 -m http.server 8000   # then open http://localhost:8000
```

## License

Code: MIT. Text, photo and résumé: all rights reserved.
