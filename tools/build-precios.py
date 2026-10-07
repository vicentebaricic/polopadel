"""Genera precios.html a partir de index.html (mismos estilos, encabezado y pie).
Uso: python3 tools/build-precios.py   (desde la raíz del repo)
Volver a correrlo cuando cambien los estilos, el encabezado o el pie de index.html."""
import re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
idx = (root / "index.html").read_text()
src = (root / "tools" / "precios.src.html").read_text()

def part(name):
    m = re.search(r"<!--\s*@" + name + r"\s*-->(.*?)<!--\s*@/" + name + r"\s*-->", src, re.S)
    return m.group(1).strip("\n")

head, style_rest = idx.split("</style>", 1)
head = re.sub(r"<title>.*?</title>", "<title>Precios · Polo Padel Chicureo</title>", head, flags=re.S)
head = re.sub(r'<meta name="description" content="[^"]*">',
              '<meta name="description" content="Cuota de socio de Polo Padel: clases por nivel, partidos, torneos y comunidad en una sola cuota mensual. Chicureo, Colina.">', head)
head += part("css") + "\n</style>\n</head>\n"

body_top = idx[idx.index('<body class="no-js">'): idx.index("<main")]
# Enlaces del menú apuntan a la portada; Precios marcado como página actual
body_top = re.sub(r'href="#(top|club|polo-system|visitanos|equipo|resenas)"', lambda m: 'href="index.html' + ("" if m.group(1)=="top" else "#"+m.group(1)) + '"', body_top)
body_top = body_top.replace('<a href="precios.html">', '<a href="precios.html" aria-current="page">')
body_top = body_top.replace('<header class="header is-over">', '<header class="header">')

foot_start = idx.index('<footer class="footer">')
foot_end = idx.index("<script>")
footer = idx[foot_start:foot_end]
footer = re.sub(r'href="#(top|club|polo-system|visitanos|equipo|resenas)"', lambda m: 'href="index.html' + ("" if m.group(1)=="top" else "#"+m.group(1)) + '"', footer)

config = re.search(r"const CONFIG = \{.*?\n\};", idx, re.S).group(0)

out = head + body_top + part("main") + "\n\n" + footer + "<script>\n" + config + "\n" + part("js") + "\n</script>\n</body>\n</html>\n"
(root / "precios.html").write_text(out)
print("precios.html", len(out), "bytes")
