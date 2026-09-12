# Recursos frontend locales

No se ejecuta Tailwind Browser ni se descargan bibliotecas/fuentes desde CDN al
abrir las páginas. Los enlaces de navegación a WhatsApp no son dependencias.

| Recurso | Versión | Archivo local | Procedencia / licencia |
| --- | --- | --- | --- |
| Tailwind CLI standalone | 4.3.3 | `.tools/v4.3.3/` (ignorado) | [Release oficial](https://github.com/tailwindlabs/tailwindcss/releases/tag/v4.3.3), MIT; SHA256 por plataforma en `tools/tailwind.lock.json` |
| Lucide | 1.17.0 | `static/js/lucide.min.js` | [lucide](https://www.npmjs.com/package/lucide/v/1.17.0), ISC y avisos incluidos en `static/licenses/lucide-LICENSE` |
| HTMX | 2.0.10 | `static/js/htmx.min.js` | [htmx.org](https://www.npmjs.com/package/htmx.org/v/2.0.10), Zero-Clause BSD |
| Alpine | 3.15.12 | `static/js/alpine.min.js` | [alpinejs](https://www.npmjs.com/package/alpinejs/v/3.15.12), MIT |
| Chart.js | 4.5.1 | `static/js/chart.umd.js` | [chart.js](https://www.npmjs.com/package/chart.js/v/4.5.1), MIT |
| Mermaid | 11.12.2 | `static/js/vendor/mermaid.min.js` | [mermaid](https://www.npmjs.com/package/mermaid/v/11.12.2), MIT |
| Source Sans 3 variable, subconjunto latino | Fontsource 5.3.0 | `static/fonts/source-sans-3/latin-wght-{normal,italic}.woff2` | [Paquete exacto](https://registry.npmjs.org/@fontsource-variable/source-sans-3/-/source-sans-3-5.3.0.tgz), SIL OFL en la misma carpeta |

Las bibliotecas JS ya estaban en el repositorio; se reutilizaron sus versiones,
identificadas por sus banners/metadatos embebidos. Se retiraron únicamente los
comentarios `sourceMappingURL` de Lucide y Chart.js porque apuntaban a mapas no
distribuidos y hacían fallar `collectstatic` con almacenamiento de manifiesto.
Las licencias de las bibliotecas se conservan en `static/licenses/`.

Las fuentes se extrajeron del paquete fijo de Fontsource, verificando la
integridad SHA512 de su tarball publicada en el registro npm. Incluyen caracteres
latinos para español y pesos variables 200–900, normal e italic. Los `url()` del
CSS fuente son relativos al destino `static/css/tailwind.css`; WhiteNoise los
reescribe al nombre con hash al recolectar estáticos.

## Actualización

1. Elegir una versión concreta de la publicación oficial y revisar su licencia.
2. Para Tailwind: actualizar versión y hashes oficiales en `tools/tailwind.lock.json`,
   ejecutar `python tools/tailwind.py install` y `build`.
3. Para bibliotecas/fuentes: reemplazar el archivo local por el artefacto verificado,
   conservar avisos y licencias, y actualizar este inventario. No usar `latest` en
   las plantillas ni introducir URLs remotas para scripts, estilos o fuentes.
4. Ejecutar pruebas, `collectstatic` y una comprobación en navegador sin acceso a
   recursos externos, incluyendo los colores tenant y fragmentos HTMX/Alpine.

La compilación no necesita conexión una vez instalado el CLI; tampoco necesita
Django ni acceso a la base de datos. Docker instala el CLI durante el build y
elimina su copia antes de la siguiente capa. El CSS compilado se versiona y se
reconstruye en cada imagen.
