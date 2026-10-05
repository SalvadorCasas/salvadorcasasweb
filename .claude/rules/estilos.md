---
paths:
  - "**/*.css"
---

# Reglas de estilos (styles.css)

## Arquitectura y tokens
- Todo el CSS vive en `styles.css`. No usar estilos inline ni `<style>` en el HTML, salvo excepciones justificadas.
- Usar SIEMPRE los tokens semánticos de `:root` (`--bg`, `--bg-alt`, `--superficie`, `--texto`, `--texto-suave`, `--borde`, `--acento`, `--sombra`) en los componentes. Nunca escribir colores directos (hex/rgb) fuera de la definición de tokens.
- Si hace falta un color nuevo, crear el token y definirlo en los 4 bloques de tema: claro por defecto, oscuro con `#tema:checked`, y sus inversos dentro de `@media (prefers-color-scheme: dark)`.
- Paleta permitida: celeste/azul a gris/negro/azul oscuro. Única excepción: `--verde-whatsapp` en el botón de WhatsApp.
- Nombres de clases en español y con convención BEM (`bloque__elemento--modificador`), igual que las existentes.
- Agrupar el archivo por secciones con comentarios `/* ---------- Nombre ---------- */`, en el mismo orden en que aparecen en el HTML.

## Modo claro y oscuro
- Todo cambio visual debe verse y leerse bien en AMBOS modos. Verificar los dos antes de dar una tarea por terminada.
- Declarar `color-scheme` en cada tema para que los controles nativos (inputs, select, scrollbar) se adapten.
- No depender del color como único indicador de estado (agregar texto, icono o borde).

## Responsive / mobile-first
- Escribir primero los estilos base para móvil y ampliar con `@media (min-width: ...)`. No usar `max-width` en media queries salvo casos puntuales.
- Breakpoints del proyecto: `768px` (tablet) y `1024px` (escritorio). No agregar otros sin necesidad.
- La página debe funcionar desde 320px de ancho sin scroll horizontal (WCAG 1.4.10 Reflow).
- Preferir layouts fluidos: `grid` con `repeat(auto-fit, minmax(...))`, `flex-wrap`, `clamp()` para tipografía y espaciados, y `max-width` en contenedores.
- Usar unidades relativas: `rem` para tipografía y espaciados, `%`/`fr` para anchos. Evitar `px` fijos en tamaños de texto.
- Para alturas de pantalla completa preferir `svh`/`dvh` (con `vh` como respaldo) para evitar saltos por la barra del navegador móvil.
- Imágenes y medios: `max-width: 100%` y `height: auto`; usar `aspect-ratio` para evitar saltos de diseño (CLS).

## Accesibilidad (WCAG 2.2 nivel AA)
- Contraste mínimo: 4.5:1 para texto normal, 3:1 para texto grande (≥ 24px o ≥ 18.66px en negrita) y para bordes/iconos de controles. Comprobarlo en ambos modos.
- Foco visible siempre: estilos en `:focus-visible` con contorno de al menos 2px y buen contraste. Nunca `outline: none` sin un reemplazo equivalente.
- El elemento con foco no debe quedar tapado por el header fijo ni por el botón de WhatsApp (WCAG 2.4.11). Mantener `scroll-margin-top` en las secciones.
- Áreas táctiles: mínimo 24×24px (WCAG 2.5.8); objetivo recomendado 44×44px para botones e iconos.
- Respetar `prefers-reduced-motion: reduce`: desactivar animaciones, transiciones largas y scroll suave.
- Contemplar `forced-colors: active` (modo de alto contraste de Windows): los bordes y el foco deben seguir visibles; usar `currentColor` en iconos SVG.
- No ocultar contenido útil con `display: none` si debe ser accesible; para ocultarlo solo visualmente usar la clase `.oculto-accesible`.
- El texto debe poder ampliarse al 200% sin cortarse ni superponerse (no fijar alturas en contenedores con texto).
- Interlineado de párrafos ≥ 1.5 y longitud de línea cómoda (≈ 60–80 caracteres, `max-width` en `ch`).

## Rendimiento y buenas prácticas
- Animar solo `transform` y `opacity`; evitar animar `width`, `height`, `top` o `box-shadow` en bucle.
- Evitar `!important`, salvo para sobrescribir estilos de accesibilidad (por ejemplo `prefers-reduced-motion`).
- Evitar selectores muy anidados o atados a IDs; preferir clases.
- Usar características modernas con buen soporte (`:has()`, `clamp()`, `gap`, `aspect-ratio`, `inset`) y asegurar una alternativa aceptable si fallan.
