# Archivos de la página · Polo Padel

Los archivos tal como se subieron quedan en `originales/`. Los de las demás carpetas ya están procesados para la web.

| Archivo | Dónde aparece | Origen |
|---|---|---|
| `marca/polo-padel-logo.png` | Encabezado y pie | logo-polo-padel.jpg, sin el fondo azul. La página lo pinta blanco o azul según el fondo |
| `marca/favicon.png`, `apple-touch-icon.png` | Pestaña del navegador / ícono en celular | Generados del logo |
| `partners/*.png` | Franja de partners | logopartner*.jpg/webp, sin fondo. La página los pasa a un solo tono gris |
| `video/entrena.*`, `conecta.*`, `compite.*` | El club (tarjetas que avanzan solas) | reel-entrena-4, reel-conecta-3, reel-compite-2. Sin audio, en MP4 y WebM, con portada `*-poster.jpg` |
| `video/garantia.*` | Banner "Nuestra convicción" | garantia.mp4, sin audio, en MP4 y WebM |
| `video/hero.*` | Fondo del hero | VIDEO-ROJAN-OK-1.mp4 (Drive), 1080p sin audio, MP4 y WebM, portada `hero-poster.jpg` |
| `fotos/hero.jpg` | Sin usar, disponible | Unsplash (Cal Gao) |
| `fotos/pala-pelota.jpg` | Polo System | Unsplash (Oskar Hagberg) |
| `fotos/cancha-palas.jpg` | Franja antes de Visítanos | Unsplash (Vincenzo Morelli) |
| `fotos/cancha.jpg` | Sin usar, disponible | Unsplash (Bruno Vaccaro) |
| `equipo/fundadora.jpg`, `head-coach.jpg`, `coach-competicion.jpg`, `comunidad.jpg` | Equipo | Capturas de Instagram (en `originales/equipo/`): sin íconos ni bordes, recorte 4:5 con la cara a la misma altura y la misma gradación. La página las muestra en gris con tono azul y a color al pasar el mouse |
| `precios.html` | Página de precios y método | Se genera con `python3 tools/build-precios.py` a partir de `tools/precios.src.html` y de los estilos, encabezado y pie de `index.html`. Volver a correrlo si cambian |
| `fotos/pala-naranja.jpg`, `partido.jpg`, `palas.jpg` | Sin usar, disponibles | Unsplash |

## Pendientes

| Archivo | Dónde aparece | Notas |
|---|---|---|

Las fotos de Unsplash son de otras canchas (una muestra un letrero "SALIDA" y edificios de otra ciudad). Conviene reemplazarlas por fotos del club con el mismo nombre de archivo.
