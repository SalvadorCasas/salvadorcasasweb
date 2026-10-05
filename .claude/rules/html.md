---
paths:
  - "**/*.html"
---

# Reglas de HTML y contenido (index.html)

## Alcance del proyecto
- El sitio es SOLO `index.html` + `styles.css`. No agregar frameworks, librerías ni archivos JS sin pedirlo antes. Si una mejora requiere JavaScript, proponerla y explicar por qué antes de implementarla.
- Respetar la estructura de secciones: Cabecera → Hero (`#inicio`) → Sobre mí (`#sobre-mi`) → Tecnologías (`#tecnologias`) → Estudios (`#estudios`) → Experiencia (`#experiencia`) → Contacto (`#contacto`) → Footer → botón flotante de WhatsApp.
- No cambiar los IDs de las secciones: los usan el menú y los enlaces internos.

## HTML semántico
- Usar etiquetas con significado: `header`, `nav`, `main`, `section`, `article`, `footer`, `ol`/`ul` para listas. Evitar `div` cuando existe una etiqueta semántica.
- Un único `<h1>` (en el hero). Jerarquía de títulos sin saltos: `h1` → `h2` (secciones) → `h3` (tarjetas o ítems).
- Mantener `<html lang="es">` y marcar con `lang` cualquier fragmento en otro idioma.
- Código válido según el validador del W3C: etiquetas cerradas, atributos entre comillas, sin IDs duplicados.
- Sangría de 2 espacios y un comentario `<!-- ===== SECCIÓN ===== -->` antes de cada bloque principal.

## Accesibilidad (WCAG 2.2 nivel AA)
- Todo elemento interactivo debe poder usarse con teclado y tener un nombre accesible: texto visible o `aria-label` en enlaces e iconos (logo, WhatsApp, hamburguesa, interruptor de tema).
- SVG decorativos con `aria-hidden="true"`. Las imágenes con contenido llevan un `alt` descriptivo; las decorativas, `alt=""`.
- Usar ARIA solo cuando el HTML nativo no alcance ("no ARIA es mejor que mal ARIA").
- Incluir un enlace "Saltar al contenido" como primer elemento del `body`, apuntando a `<main id="contenido">`.
- El orden del código debe coincidir con el orden visual y el de navegación con Tab.
- Enlaces con texto que se entienda fuera de contexto (evitar "click aquí"). Si abren en otra pestaña, indicarlo (por ejemplo, en el `aria-label`).
- No bloquear el zoom: el meta viewport no debe llevar `user-scalable=no` ni `maximum-scale`.

## Formulario de contacto
- No modificar el `action` (`https://formsubmit.co/contacto@salvadorcasas.com.ar`), el `method="POST"` ni los campos ocultos de FormSubmit (`_subject`, `_template`, `_captcha`, `_honey`) sin confirmación.
- Cada campo con su `<label for>` visible; no usar el `placeholder` como única etiqueta.
- Usar el `type` correcto (`email`, `tel`, etc.), `autocomplete` adecuado (`name`, `email`) y `required` en los obligatorios.
- El campo de correo debe llamarse `name="email"` (FormSubmit lo usa como dirección de respuesta).

## SEO y metadatos
- Mantener `<title>` y `<meta name="description">` actualizados con el perfil (máx. ~60 y ~155 caracteres).
- Agregar etiquetas Open Graph (`og:title`, `og:description`, `og:type`, `og:url`, `og:image`) cuando el sitio tenga dominio publicado.
- Enlaces externos con `target="_blank"` deben llevar `rel="noopener noreferrer"`.

## Rendimiento
- Imágenes con `width` y `height` explícitos, `loading="lazy"` (salvo las visibles al cargar) y formatos modernos (WebP/AVIF) con buen tamaño de compresión.
- Fuentes de Google con `preconnect` y `display=swap`. No cargar más pesos de fuente de los que se usan.

## Contenido y tono
- Fuente de verdad: el CV de Salvador. No inventar experiencia, cargos, fechas, certificaciones, herramientas ni logros. Si falta un dato, dejarlo pendiente y preguntar.
- Idioma: español rioplatense con voseo, de forma coherente en todo el sitio ("Contactame", "Escribime", "Elegí").
- Tono profesional, cercano y concreto. Frases cortas, voz activa y verbos de acción ("Relevé", "Diseñé", "Coordiné"). Evitar relleno y frases vacías ("apasionado por la excelencia").
- Destacar logros y valor aportado por sobre la simple lista de tareas; usar datos medibles solo si el CV los incluye.
- Revisar ortografía y tildes en todo texto nuevo.
- Formatos consistentes:
  - Fechas: `Mes AAAA – Mes AAAA` o `Mes AAAA – Actualidad`, con raya (–) y mes con mayúscula inicial.
  - Nombres de herramientas con su grafía oficial: JavaScript, PostgreSQL, DBeaver, GitLab, SuiteCRM, Botmaker, Playwright, Postman.
- Orden cronológico inverso en Experiencia y Estudios (lo más reciente primero).

## Privacidad
- No mostrar en el sitio el correo personal (Gmail) ni el número de teléfono en texto visible. El contacto público es `contacto@salvadorcasas.com.ar` y el número solo va dentro del enlace de WhatsApp (`https://wa.me/5493516983776`).
- No publicar dirección exacta: solo "Córdoba Capital, Argentina".
