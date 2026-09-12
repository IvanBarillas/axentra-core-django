"""Regresiones de CSS compilado y recursos locales, sin acceder a la BD."""
import re
from pathlib import Path
from types import SimpleNamespace

from django.conf import settings
from django.contrib.staticfiles import finders
from django.template.loader import render_to_string
from django.test import SimpleTestCase, override_settings


class FrontendAssetsTests(SimpleTestCase):
    def test_templates_do_not_load_remote_libraries(self):
        for root in ('templates', 'apps'):
            for path in (settings.BASE_DIR / root).rglob('*.html'):
                content = path.read_text()
                with self.subTest(template=path):
                    self.assertNotRegex(content, r'<(?:script|link)\b[^>]*(?:src|href)=["\'](?:https?:)?//')
                    self.assertNotIn('text/tailwindcss', content)
                    self.assertNotIn('@import', content)

    def test_css_includes_dynamic_cards_and_interaction_states(self):
        css = (settings.BASE_DIR / 'static/css/tailwind.css').read_text()
        self.assertNotIn('@import', css)
        self.assertNotIn('@theme', css)
        # Colores realmente pasados a stats_card y su valor por defecto.
        for color in ('blue-600', 'slate-600', 'emerald-600', 'red-600', 'brand-accent'):
            for candidate in (f'group-hover:bg-{color}', f'group-hover:text-{color}', f'hover:border-{color}/30'):
                selector = '.' + re.sub(r'([^a-zA-Z0-9_-])', r'\\\1', candidate)
                self.assertIn(selector, css, candidate)
        for candidate in ('hidden', 'opacity-0', 'rotate-180', 'bg-brand-primary', 'bg-brand-accent/10'):
            selector = '.' + re.sub(r'([^a-zA-Z0-9_-])', r'\\\1', candidate)
            self.assertIn(selector, css, candidate)
        self.assertIn('var(--color-brand-primary)', css)

    def test_css_font_references_resolve_locally(self):
        css_path = Path(finders.find('css/tailwind.css'))
        urls = re.findall(r'url\(["\']?([^\)"\']+)', css_path.read_text())
        self.assertEqual(len(urls), 2)
        for url in urls:
            self.assertFalse(url.startswith(('http:', 'https:', '//')))
            path = (css_path.parent / url).resolve()
            self.assertTrue(path.is_relative_to(settings.BASE_DIR / 'static'))
            self.assertEqual(path.read_bytes()[:4], b'wOF2')

    @override_settings(DEBUG=True)
    def test_standalone_pages_keep_tenant_colors_without_compilation(self):
        tenant = SimpleNamespace(primary_color='#123456', secondary_color='#654321', accent_color='#abcdef')
        for page in ('registration/login.html', 'public/index.html', 'errors/403.html', 'errors/404.html'):
            html = render_to_string(page, {'tenant': tenant})
            with self.subTest(page=page):
                self.assertIn('--color-brand-primary: #123456;', html)
                self.assertIn('--color-brand-accent: #abcdef;', html)
                self.assertIn('/static/css/tailwind.css', html)
                self.assertIn('/static/js/lucide.min.js', html)
                self.assertNotIn('@theme', html)
