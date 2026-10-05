"""
Revisa y limpia los metadatos de las imágenes del sitio.

Los metadatos son datos ocultos dentro de un archivo: ubicación GPS, modelo de cámara
o de celular, fecha, nombre del autor, programa usado, perfiles de color con el nombre
del monitor, o registros de procedencia (C2PA). No se ven en la página, pero cualquiera
que descargue el archivo puede leerlos.

Uso (desde la carpeta del proyecto):
    python _herramientas/metadatos.py            -> solo revisa y muestra lo que encuentra
    python _herramientas/metadatos.py --limpiar  -> además lo borra (modifica los archivos)

Formatos: PNG, WebP, JPEG y SVG. Quita solo los bloques de metadatos: la imagen
no se vuelve a comprimir, así que no pierde calidad.
No necesita instalar nada (solo Python 3).
"""

import re
import struct
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
# Carpetas que no se publican o no son del sitio
EXCLUIDAS = {".git", ".claude", "_originales", "_herramientas", "node_modules"}

# PNG: bloques técnicos que no contienen datos personales y se conservan
PNG_CONSERVAR = {b"IHDR", b"PLTE", b"IDAT", b"IEND", b"tRNS", b"sRGB", b"gAMA",
                 b"cHRM", b"pHYs", b"sBIT", b"acTL", b"fcTL", b"fdAT"}
# WebP: bloques de metadatos que se quitan (perfil de color, EXIF y XMP)
WEBP_QUITAR = {b"ICCP", b"EXIF", b"XMP "}


def revisar_png(datos):
    if datos[:8] != b"\x89PNG\r\n\x1a\n":
        return datos, ["no parece un PNG válido"]
    salida, encontrados, pos = bytearray(datos[:8]), [], 8
    while pos < len(datos):
        largo = struct.unpack(">I", datos[pos:pos + 4])[0]
        tipo = datos[pos + 4:pos + 8]
        bloque = datos[pos:pos + 12 + largo]
        if tipo in PNG_CONSERVAR:
            salida += bloque
        else:
            encontrados.append(f"bloque {tipo.decode('latin-1')} ({largo} bytes)")
        pos += 12 + largo
        if tipo == b"IEND":
            break
    return bytes(salida), encontrados


def revisar_webp(datos):
    if datos[:4] != b"RIFF" or datos[8:12] != b"WEBP":
        return datos, ["no parece un WebP válido"]
    cuerpo, encontrados, pos = bytearray(), [], 12
    while pos + 8 <= len(datos):
        tipo = datos[pos:pos + 4]
        largo = struct.unpack("<I", datos[pos + 4:pos + 8])[0]
        bloque = datos[pos:pos + 8 + largo + (largo & 1)]
        if tipo in WEBP_QUITAR:
            encontrados.append(f"bloque {tipo.decode('latin-1').strip()} ({largo} bytes)")
        else:
            cuerpo += bloque
        pos += 8 + largo + (largo & 1)
    if encontrados and cuerpo[:4] == b"VP8X":
        # Apaga los avisos de "tiene ICC / EXIF / XMP" en la cabecera extendida
        cuerpo[8] &= ~(0x20 | 0x08 | 0x04) & 0xFF
    salida = b"RIFF" + struct.pack("<I", len(cuerpo) + 4) + b"WEBP" + bytes(cuerpo)
    return salida, encontrados


def revisar_jpeg(datos):
    if datos[:2] != b"\xff\xd8":
        return datos, ["no parece un JPEG válido"]
    salida, encontrados, pos = bytearray(b"\xff\xd8"), [], 2
    while pos + 4 <= len(datos):
        marca = datos[pos + 1]
        if marca == 0xDA:  # inicio de la imagen comprimida: se copia el resto tal cual
            salida += datos[pos:]
            break
        largo = struct.unpack(">H", datos[pos + 2:pos + 4])[0]
        segmento = datos[pos:pos + 2 + largo]
        # APP1-APP13 y APP15 (EXIF, XMP, ICC, IPTC...) y comentarios. APP0 (JFIF) y APP14 (Adobe) son técnicos.
        if (0xE1 <= marca <= 0xEF and marca != 0xEE) or marca == 0xFE:
            encontrados.append(f"segmento APP{marca - 0xE0} ({largo} bytes)" if marca != 0xFE else f"comentario ({largo} bytes)")
        else:
            salida += segmento
        pos += 2 + largo
    return bytes(salida), encontrados


SVG_PATRONES = [
    (re.compile(r"<metadata\b.*?</metadata>", re.S), "bloque <metadata>"),
    (re.compile(r"<!--.*?-->", re.S), "comentario"),
    (re.compile(r"<sodipodi:namedview\b.*?(/>|</sodipodi:namedview>)", re.S), "datos de Inkscape"),
    (re.compile(r'\s+xmlns:(c2pa|inkscape|sodipodi|rdf|dc|cc)="[^"]*"'), "espacio de nombres de metadatos"),
    (re.compile(r'\s+(inkscape|sodipodi):[\w-]+="[^"]*"'), "atributo de Inkscape"),
]


def revisar_svg(datos):
    texto = datos.decode("utf-8")
    encontrados = []
    for patron, nombre in SVG_PATRONES:
        cantidad = len(patron.findall(texto))
        if cantidad:
            encontrados.append(f"{nombre} (x{cantidad})")
            texto = patron.sub("", texto)
    return texto.encode("utf-8"), encontrados


REVISORES = {".png": revisar_png, ".webp": revisar_webp, ".jpg": revisar_jpeg,
             ".jpeg": revisar_jpeg, ".svg": revisar_svg}
SIN_SOPORTE = {".gif", ".avif", ".heic", ".tif", ".tiff", ".mp4", ".webm", ".mov"}


def main():
    limpiar = "--limpiar" in sys.argv
    con_metadatos, revisados = 0, 0
    for archivo in sorted(RAIZ.rglob("*")):
        if not archivo.is_file() or EXCLUIDAS & set(archivo.relative_to(RAIZ).parts):
            continue
        extension = archivo.suffix.lower()
        ruta = archivo.relative_to(RAIZ).as_posix()
        if extension in SIN_SOPORTE:
            print(f"  ?  {ruta}: formato no soportado por este script, revisarlo con otra herramienta (por ejemplo, ffmpeg o exiftool)")
            continue
        if extension not in REVISORES:
            continue
        revisados += 1
        datos = archivo.read_bytes()
        limpio, encontrados = REVISORES[extension](datos)
        if not encontrados:
            print(f"  OK {ruta}")
            continue
        con_metadatos += 1
        print(f"  !! {ruta}: " + ", ".join(encontrados))
        if limpiar:
            archivo.write_bytes(limpio)
            print(f"     -> limpiado ({len(datos)} -> {len(limpio)} bytes)")
    print(f"\n{revisados} archivos revisados, {con_metadatos} con metadatos.")
    if con_metadatos and not limpiar:
        print("Para quitarlos: python _herramientas/metadatos.py --limpiar")
    return 1 if con_metadatos and not limpiar else 0


if __name__ == "__main__":
    sys.exit(main())
