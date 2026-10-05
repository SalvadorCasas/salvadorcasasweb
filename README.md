# salvadorcasasweb
Sitio web de mi Perfil Profesional

## Cómo verlo
Abrir `index.html` con la extensión **Live Server** de VS Code (o cualquier servidor http).
Abriendo el archivo directo (`file://`), el navegador bloquea la fuente local y la consola muestra errores que no existen en el sitio publicado.

## Antes de agregar imágenes
Todas las imágenes se publican sin metadatos (ubicación, cámara, autor, etc.). Después de agregar una, correr:

```
python _herramientas/metadatos.py --limpiar
```

## Al cambiar los estilos
Cada vez que se modifica `styles.css`, actualizar la fecha en `index.html` (`styles.css?v=AAAAMMDD`). Así los navegadores descargan el CSS nuevo en lugar de usar el guardado.

## Estructura
- `index.html` y `styles.css`: el sitio (HTML y CSS, sin JavaScript).
- `img/` y `fuentes/`: imágenes y la fuente Inter (licencia en `fuentes/OFL-inter.txt`).
- `.htaccess`: HTTPS y cabeceras de seguridad para el hosting.
- `_herramientas/`: herramientas de desarrollo; no forman parte del sitio.
