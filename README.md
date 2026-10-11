# Polo Padel · sitio web

Sitio de Polo Padel (Chicureo, Colina). Se genera con la plantilla de clubes de pádel, que vive en el repo `plantilla-padel`.

| Archivo | Qué es |
|---|---|
| `club.yml` | **Todo lo propio del club**: contacto, links, equipo, partners, horarios, precios, paleta y perillas de diseño. Aquí se hacen los cambios. |
| `assets/` | Logo, fotos, videos y logos de partners (detalle en `assets/LEEME.md`). |
| `index.html`, `precios.html` | Sitio publicado. **No editar a mano**: se generan desde `club.yml`. |

## Hacer un cambio

1. Edita `club.yml` (o reemplaza archivos en `assets/` manteniendo el nombre).
2. Con los dos repos clonados uno al lado del otro, regenera el sitio:

   ```
   python3 ../plantilla-padel/build.py club.yml
   ```

3. Sube los cambios (`club.yml`, `assets/` y los dos HTML generados).
