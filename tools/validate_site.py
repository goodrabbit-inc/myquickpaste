"""Validate the actual Pages bundle, including assets referenced by the hub.

Run from the repository: python tools/validate_site.py _site
"""
import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse

BASE = "https://goodrabbit-inc.github.io/myquickpaste/"
ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()


def require(condition, message):
    if not condition:
        raise SystemExit(message)


def local_file(url):
    parsed = urlparse(url)
    if parsed.netloc != urlparse(BASE).netloc:
        return None
    prefix = urlparse(BASE).path
    if not parsed.path.startswith(prefix):
        return None
    relative = unquote(parsed.path[len(prefix):])
    if not relative or relative.endswith("/"):
        relative += "index.html"
    resolved = (ROOT / relative).resolve()
    require(resolved.is_relative_to(ROOT), f"Path outside site: {url}")
    return resolved


class Page(HTMLParser):
    def __init__(self, route):
        super().__init__()
        self.route = route
        self.canonical = []
        self.hreflang = []
        self.h1_count = 0
        self.description = False
        self.has_title = False
        self.schema = []
        self.schema_text = None

    def handle_starttag(self, tag, attrs):
        attr = dict(attrs)
        if tag == "h1":
            self.h1_count += 1
        if tag == "title":
            self.has_title = True
        if tag == "meta" and attr.get("name") == "description":
            self.description = bool(attr.get("content"))
        if tag == "link" and attr.get("rel") == "canonical":
            self.canonical.append(attr.get("href"))
        if tag == "link" and attr.get("hreflang"):
            self.hreflang.append(attr)
        if tag == "script" and attr.get("type") == "application/ld+json":
            self.schema_text = ""
        if self.route == "":
            references = []
            if tag in ("img", "script") and attr.get("src"):
                references.append(attr["src"])
            if tag in ("link", "a") and attr.get("href"):
                references.append(attr["href"])
            if tag == "meta" and attr.get("property") == "og:image":
                references.append(attr.get("content", ""))
            for ref in references:
                resolved = local_file(urljoin(BASE + self.route, ref))
                if resolved is not None:
                    require(resolved.is_file(), f"Missing deployed asset/link: {ref}")
            if tag == "img":
                require(bool(attr.get("alt")), "Hub image missing alt text")
                require(attr.get("width") and attr.get("height"), "Hub image missing dimensions")

    def handle_data(self, data):
        if self.schema_text is not None:
            self.schema_text += data

    def handle_endtag(self, tag):
        if tag == "script" and self.schema_text is not None:
            self.schema.append(json.loads(self.schema_text))
            self.schema_text = None


for route in ("", "windows/", "android/"):
    source = local_file(BASE + route).read_text(encoding="utf-8")
    page = Page(route)
    page.feed(source)
    require(page.canonical == [BASE + route], f"Invalid canonical: {route}")
    require(page.h1_count == 1, f"Expected one H1: {route}")
    require(page.has_title and page.description and page.schema, f"SEO metadata missing: {route}")
    require(len(page.hreflang) == 22, f"Language alternates missing: {route}")
    require(not re.search(r'<meta[^>]+name="robots"[^>]+noindex', source), f"Indexing blocked: {route}")
    if not route:
        for alternate in page.hreflang:
            lang = alternate["hreflang"].lower()
            if lang == "x-default":
                continue
            translations = json.loads((ROOT / "i18n" / f"{lang}.json").read_text(encoding="utf-8"))
            require(translations["hub"]["windowsTitle"] and translations["hub"]["androidTitle"], f"Missing hub text: {lang}")
            android_locale = {"zh-cn": "zh", "zh-tw": "zh_TW"}.get(lang, lang)
            for image in (f"images/windows-ads/{lang}-Windows_frequent-text_one-click_1024x500.png", f"android/images/marketing/feature-{android_locale}.png"):
                require((ROOT / image).is_file(), f"Missing translated image: {image}")

sitemap = ET.parse(ROOT / "sitemap.xml")
urls = {n.text for n in sitemap.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc")}
require({BASE, BASE + "windows/", BASE + "android/"}.issubset(urls), "Missing edition route in sitemap")
require(not any("/business/" in url for url in urls), "Legacy business URL in sitemap")
require("Sitemap: " + BASE + "sitemap.xml" in (ROOT / "robots.txt").read_text(encoding="utf-8"), "Missing robots sitemap directive")
redirect = (ROOT / "business/index.html").read_text(encoding="utf-8")
require('http-equiv="refresh"' in redirect and BASE + "android/" in redirect and "noindex,follow" in redirect, "Legacy redirect broken")
print("Pages bundle OK: hub assets, 21 locales, edition routes, metadata, JSON-LD, sitemap, robots, legacy redirect")
