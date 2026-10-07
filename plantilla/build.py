#!/usr/bin/env python3
"""Genera el sitio de un club de pádel a partir de la plantilla.

Uso (desde la carpeta plantilla/):
    python3 build.py clubes/polo-padel/club.yml
    python3 build.py clubes/demo/club.yml --salida sitios/demo

Lee los textos genéricos (textos.yml), los datos del club (club.yml) y los
estilos elegidos (estilos.yml), y escribe index.html y precios.html.
Requiere: pip install jinja2 pyyaml
"""
import argparse, colorsys, copy, json, pathlib, re, shutil, sys

import yaml
from jinja2 import ChainableUndefined, Environment, FileSystemLoader

ROOT = pathlib.Path(__file__).resolve().parent


# ---------------------------------------------------------------- utilidades
def deep_merge(base, extra):
    """Mezcla diccionarios: lo del club pisa lo genérico."""
    out = copy.deepcopy(base)
    for k, v in (extra or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out


def pick_variants(node, variante):
    """En textos.yml, un bloque "variantes:" ofrece varias versiones de un texto: se elige una por club."""
    if isinstance(node, dict) and set(node) == {"variantes"}:
        opciones = node["variantes"]
        return pick_variants(opciones[(variante - 1) % len(opciones)], variante)
    if isinstance(node, dict):
        return {k: pick_variants(v, variante) for k, v in node.items()}
    if isinstance(node, list):
        return [pick_variants(x, variante) for x in node]
    return node


def fill(node, vars_):
    """Reemplaza {club}, {barrio}, {metodo}… en todos los textos."""
    if isinstance(node, dict):
        return {k: fill(v, vars_) for k, v in node.items()}
    if isinstance(node, list):
        return [fill(x, vars_) for x in node]
    if isinstance(node, str):
        return re.sub(r"\{(\w+)\}", lambda m: str(vars_.get(m.group(1), m.group(0))), node)
    return node


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return "#" + "".join(f"{max(0, min(255, round(c))):02X}" for c in rgb)


def hsl(h, dl=0.0, s=None, l=None):
    """Ajusta la luminosidad (o fija saturación / luminosidad) conservando el tono."""
    r, g, b = (c / 255 for c in hex_to_rgb(h))
    hh, ll, ss = colorsys.rgb_to_hls(r, g, b)
    ll = l if l is not None else min(1, max(0, ll + dl))
    ss = s if s is not None else ss
    return rgb_to_hex(c * 255 for c in colorsys.hls_to_rgb(hh, ll, ss))


def mix(a, b, t):
    ra, rb = hex_to_rgb(a), hex_to_rgb(b)
    return rgb_to_hex(x + (y - x) * t for x, y in zip(ra, rb))


def rgba(h, a):
    r, g, b = hex_to_rgb(h)
    return f"rgba({r},{g},{b},{a})"


def tokens(p):
    """Deriva todos los colores de la página desde los 4–6 colores de marca del club."""
    marca, oscuro, acento = p["marca"], p["oscuro"], p["acento"]
    tono, tono_osc = p["tono"], p.get("tono_oscuro", hsl(p["tono"], -0.12))
    crema, claro = p.get("crema", "#F5F1E8"), p.get("fondo_claro", "#FBFAF6")
    profundo = hsl(oscuro, -0.04)
    t = {
        "base": dict(brand=marca, navy=oscuro, **{"navy-deep": profundo}, ball=acento, wood=tono,
                     earth=tono_osc, cream=crema),
        # Propuesta clara: domina el blanco
        "clara": {
            "bg": claro, "bg-alt": mix(claro, tono, .07), "surface": "#FFFFFF", "surface-2": mix(claro, tono, .15),
            "text": oscuro, "text-2": mix(oscuro, "#FFFFFF", .2), "text-3": mix(oscuro, "#FFFFFF", .33),
            "line": rgba(oscuro, .13), "hl": "var(--brand)", "tone": "var(--earth)",
            "btn-bg": "var(--brand)", "btn-text": "#FFFFFF", "logo": "var(--brand)",
            "header-bg": rgba(claro, .92), "placeholder-a": mix(claro, tono, .12), "placeholder-b": mix(claro, tono, .2),
            "partner-filter": "brightness(0) opacity(.42)", "focus": "var(--brand)",
        },
        # Propuesta de marca: domina el color principal
        "marca": {
            "bg": marca, "bg-alt": hsl(marca, -0.04), "surface": hsl(marca, 0.05), "surface-2": hsl(marca, 0.1),
            "text": crema, "text-2": hsl(marca, l=.84, s=.3), "text-3": hsl(marca, l=.72, s=.28),
            "line": rgba(crema, .14), "hl": "var(--ball)", "tone": "var(--wood)",
            "btn-bg": "var(--ball)", "btn-text": "var(--navy)", "logo": "#FFFFFF",
            "header-bg": rgba(marca, .94), "placeholder-a": hsl(marca, 0.05), "placeholder-b": hsl(marca, 0.1),
            "partner-filter": "brightness(0) invert(1) opacity(.55)", "focus": "var(--ball)",
        },
        # Oscuro de la propuesta clara: gris carbón neutro
        "clara_oscura": {
            "bg": "#121417", "bg-alt": "#181B1F", "surface": "#1F2328", "surface-2": "#272C33",
            "text": "#F2EFE8", "text-2": "#C3CBD8", "text-3": "#A0AABB", "line": "rgba(242,239,232,.12)",
            "hl": "var(--ball)", "tone": "var(--wood)", "btn-bg": "var(--ball)", "btn-text": "var(--navy)",
            "header-bg": "rgba(18,20,23,.92)", "placeholder-a": "#1F2328", "placeholder-b": "#272C33",
            "partner-filter": "brightness(0) invert(1) opacity(.5)", "focus": "var(--ball)", "logo": "#FFFFFF",
        },
        # Oscuro de la propuesta de marca: el mismo tono, muy profundo
        "marca_oscura": {
            "bg": hsl(marca, l=.09), "bg-alt": hsl(marca, l=.12), "surface": hsl(marca, l=.16), "surface-2": hsl(marca, l=.2),
            "header-bg": rgba(hsl(marca, l=.09), .92), "placeholder-a": hsl(marca, l=.16), "placeholder-b": hsl(marca, l=.2),
        },
    }
    for k, v in (p.get("ajustes") or {}).items():   # ajustes finos por club, si hicieran falta
        t[k].update(v)
    return t


def fs_scale(base, f):
    """Escala un clamp(min, vw, max) por el factor de la tipografía."""
    a, b, c = base
    return f"clamp({a * f:.3f}rem, {b * f:.2f}vw, {c * f:.3f}rem)"


# ---------------------------------------------------------------- armado
def build(club_path, salida=None):
    club_path = pathlib.Path(club_path).resolve()
    club_dir = club_path.parent
    estilos = yaml.safe_load((ROOT / "estilos.yml").read_text())
    club = yaml.safe_load(club_path.read_text())
    e = club["estilo"]

    # Aviso si otro club ya usa exactamente la misma combinación de perillas
    PERILLAS = ("tipografia", "forma", "hero", "etiquetas", "variante_textos")
    combo = tuple(e.get(k) for k in PERILLAS)
    for otro in (ROOT / "clubes").glob("*/club.yml"):
        if otro.resolve() == club_path:
            continue
        oe = (yaml.safe_load(otro.read_text()) or {}).get("estilo", {})
        if tuple(oe.get(k) for k in PERILLAS) == combo:
            print(f"  ⚠ {otro.parent.name} usa la misma combinación ({', '.join(map(str, combo))}). "
                  "Cambia al menos una perilla para que no se parezcan.")

    tipo = estilos["tipografias"][e["tipografia"]]
    forma = estilos["formas"][e["forma"]]

    variables = dict(club=club["nombre"], barrio=club["ubicacion"]["barrio"], comuna=club["ubicacion"]["comuna"],
                     metodo=club.get("metodo", {}).get("nombre", "nuestro método"),
                     dias=club.get("garantia", {}).get("dias", 90))
    textos = yaml.safe_load((ROOT / "textos.yml").read_text())
    textos = deep_merge(textos, club.get("textos"))
    textos = fill(pick_variants(textos, int(e.get("variante_textos", 1))), variables)

    secciones = e.get("secciones") or estilos["secciones_por_defecto"]
    # Número de cada sección para las etiquetas (/01, /02…)
    numeradas = [s for s in secciones if s not in ("partners", "banda", "cta")]
    numeros = {s: f"{i + 1:02d}" for i, s in enumerate(numeradas)}

    ctx = dict(
        club=club, T=textos, E=e, tipo=tipo, forma=forma, secciones=secciones, num=numeros,
        tok=tokens(club["paleta"]),
        fs=dict(h1=fs_scale((2.75, 9, 6.75), tipo["escala"]), h2=fs_scale((2.125, 5.4, 4), tipo["escala"]),
                h3=fs_scale((1.375, 2.4, 1.75), tipo["escala"])),
        slug=club["slug"], json=json,
    )

    env = Environment(loader=FileSystemLoader(ROOT / "templates"), undefined=ChainableUndefined,
                      trim_blocks=True, lstrip_blocks=True, autoescape=False)
    out = pathlib.Path(salida or club.get("salida") or (ROOT / "sitios" / club["slug"]))
    if not out.is_absolute():
        out = (club_dir / out).resolve() if salida is None and club.get("salida") else (pathlib.Path.cwd() / out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    for page in ("index", "precios"):
        if page == "precios" and not club.get("precios"):
            continue
        html = env.get_template(f"{page}.html.j2").render(page=page, **ctx)
        (out / f"{page}.html").write_text(html)
        print(f"  {out / (page + '.html')}  ({len(html) // 1024} KB)")

    # Copia los archivos del club si viven en otra carpeta
    assets = club.get("assets")
    if assets:
        src = (club_dir / assets).resolve()
        dst = out / "assets"
        if src != dst.resolve():
            shutil.copytree(src, dst, dirs_exist_ok=True, ignore=shutil.ignore_patterns("originales"))
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("club", help="ruta al club.yml")
    ap.add_argument("--salida", help="carpeta de salida (por defecto la indicada en club.yml o sitios/<slug>)")
    a = ap.parse_args()
    print("Generando", a.club)
    build(a.club, a.salida)
