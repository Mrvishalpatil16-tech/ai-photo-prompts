"""Build index.html + sitemap.xml from template.html and prompts.json.

Run:  python3 build.py
Pre-renders the prompt list into the HTML (so search engines can read it without
JavaScript) and adds JSON-LD structured data. Run this whenever
prompts.json changes (run it after owner edits to refresh the SEO copy).
"""
import datetime
import html
import json
import pathlib

ROOT = pathlib.Path(__file__).parent
URL = "https://mrvishalpatil16-tech.github.io/ai-photo-prompts/"


def build():
    prompts = json.loads((ROOT / "prompts.json").read_text(encoding="utf-8"))
    uniq = [p for p in prompts if not p.get("dup")]

    pre = "".join(
        f'<article class="card" id="p-{html.escape(p["id"])}"><div class="body">'
        f'<h3>{html.escape(p["title"])}</h3><div class="text">{html.escape(p["text"])}</div>'
        f"</div></article>"
        for p in uniq
    )
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "WebSite", "@id": URL + "#site", "name": "AI Photo Prompts", "url": URL, "inLanguage": "en"},
            {
                "@type": "CollectionPage",
                "@id": URL + "#page",
                "url": URL,
                "name": "AI Photo Prompts — copy-paste prompts for portraits, posters & couple photos",
                "isPartOf": {"@id": URL + "#site"},
                "primaryImageOfPage": URL + "og-image.png",
                "mainEntity": {
                    "@type": "ItemList",
                    "numberOfItems": len(uniq),
                    "itemListElement": [
                        {
                            "@type": "ListItem",
                            "position": i + 1,
                            "item": {
                                "@type": "CreativeWork",
                                "name": p["title"],
                                "url": f'{URL}#p-{p["id"]}',
                                "description": p["text"][:200],
                                "keywords": ", ".join(p.get("tags") or []),
                            },
                        }
                        for i, p in enumerate(uniq)
                    ],
                },
            },
        ],
    }
    out = (
        (ROOT / "template.html").read_text(encoding="utf-8")
        .replace("__LD__", json.dumps(ld, ensure_ascii=False).replace("</", "<\\/"))
        .replace("__PRE__", pre)
        .replace("__DATA__", json.dumps(prompts, ensure_ascii=False).replace("</", "<\\/"))
    )
    assert "__LD__" not in out and "__PRE__" not in out and "__DATA__" not in out
    (ROOT / "index.html").write_text(out, encoding="utf-8")

    today = datetime.date.today().isoformat()
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"  <url><loc>{URL}</loc><lastmod>{today}</lastmod><changefreq>weekly</changefreq><priority>1.0</priority></url>\n"
        "</urlset>\n",
        encoding="utf-8",
    )
    print(f"built index.html ({len(uniq)} prompts) + sitemap.xml")


if __name__ == "__main__":
    build()
