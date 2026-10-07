# Plantilla de sitios para clubes de pádel

Una sola plantilla con todo lo genérico (estructura, animaciones, pilares con video, método, garantía, precios, WhatsApp, modo claro/oscuro) y un archivo de datos por club. El generador arma `index.html` y `precios.html` de cada club.

```
plantilla/
├── build.py              → generador
├── textos.yml            → textos genéricos de un club de pádel (con variantes)
├── estilos.yml           → perillas de diseño: tipografías, formas, secciones
├── templates/            → HTML, CSS y JS genéricos (no se tocan por club)
├── clubes/
│   ├── polo-padel/club.yml   → Polo Padel (se publica en la raíz del repo)
│   └── demo/club.yml         → club ficticio para mostrar otra combinación
└── sitios/               → sitios generados que no tienen otra salida (ej. sitios/demo)
```

## Crear el sitio de un club nuevo

1. Copia `clubes/demo/` como `clubes/<nombre-del-club>/` y edita su `club.yml`:
   - **Datos:** nombre, WhatsApp, link de reservas (EasyCancha, Playtomic…), Instagram, dirección, horarios.
   - **Archivos:** logo (PNG sin fondo), fotos del equipo, partners, videos o fotos del héroe y de los pilares.
   - **Precios:** tamaños de grupo y valores mensual y anual.
   - **Paleta:** el color del logo (`marca`), uno oscuro, un acento y un tono. El resto de los colores se calcula solo.
   - **Perillas de estilo:** ver abajo.
   - Marca con `muestra: true` (o un texto) todo lo que sea de ejemplo: aparece la etiqueta "Contenido de ejemplo".
2. Genera: `python3 build.py clubes/<nombre-del-club>/club.yml` (requiere `pip install jinja2 pyyaml`).
3. Revisa el resultado en `sitios/<slug>/` o en la carpeta indicada en `salida:`.

Cualquier texto genérico se puede reescribir para un club en su `club.yml`, bajo `textos:` (mismas claves que `textos.yml`).

> Polo Padel ya se genera desde aquí: si editas su `club.yml` o la plantilla, vuelve a correr
> `python3 build.py clubes/polo-padel/club.yml` y se actualizan `index.html` y `precios.html` de la raíz.

## Cómo evitar que los sitios se parezcan

Todos comparten estructura y mensaje, pero cada club combina perillas distintas en `estilo:`:

| Perilla | Opciones | Qué cambia |
|---|---|---|
| `paleta` | colores del logo | Todo el color del sitio, en sus dos propuestas (marca y clara) |
| `tipografia` | `deportiva` · `condensada` · `geometrica` · `limpia` | Títulos, textos y cifras: lo que más cambia la personalidad |
| `forma` | `redonda` · `suave` · `recta` | Esquinas de tarjetas, fotos y botones |
| `hero` | `completo` · `dividido` | Video a pantalla completa, o texto al lado de un recuadro con video/foto |
| `etiquetas` | `barra` · `numero` · `simple` | "/01 El club", "01 — El club" o "— El club" |
| `variante_textos` | `1` · `2` · `3` | Titulares y bajadas alternativos (ninguno repite la misma frase) |
| `secciones` | orden y cuáles van | Recorrido de la página (p. ej. equipo antes que la garantía, sin franja de foto) |
| `menu` | qué aparece arriba | Énfasis distinto en cada club |

Solo con las perillas fijas hay 4 × 3 × 2 × 3 × 3 = **216 combinaciones**, antes de contar paleta, orden de secciones y contenido propio. El generador avisa si dos clubes quedan con la misma combinación.

Además de las perillas, lo que más diferencia un sitio:

- **Contenido real:** fotos y videos propios del club (no de stock), su equipo y reseñas reales.
- **Nombre propio del método y de los pilares:** "Polo System", "Método Arena"… y, si el club lo pide, otros pilares en vez de Entrena / Conecta / Compite (`textos.club.pilares`).
- **Zona:** si dos clientes están cerca uno del otro, que no compartan tipografía ni héroe.

## Registro de clubes

| Club | Tipografía | Forma | Héroe | Etiquetas | Textos |
|---|---|---|---|---|---|
| Polo Padel | deportiva | redonda | completo | barra | 1 |
| Demo (Arena Pádel Club) | condensada | recta | dividido | numero | 2 |

## Para crecer más adelante

Las variantes nuevas se agregan una vez a la plantilla y quedan disponibles para todos: otro estilo de héroe (carrusel de fotos), pilares en pestañas en vez de tarjetas, una sección de clases infantiles, una galería, etc.
