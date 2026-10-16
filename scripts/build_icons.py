"""Descarga/genera los íconos del stack en assets/icons/, todos con el mismo estilo de recuadro (skill-icons).

- Los que existen en skill-icons se descargan tal cual.
- Los que no (IA, PostHog...) se arman con el logo de Simple Icons sobre el mismo recuadro.

Uso:  python scripts/build_icons.py
Para añadir uno: agrégalo a SKILL_ICONS o SIMPLE_ICONS y vuelve a correr el script.
"""
import re
import urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets" / "icons"

SKILL = "https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/{}.svg"
SIMPLE = "https://cdn.jsdelivr.net/npm/simple-icons@{}/icons/{}.svg"

# nombre local -> archivo en skill-icons
SKILL_ICONS = {
    "python": "Python-Dark", "java": "Java-Dark", "cpp": "CPP", "javascript": "JavaScript",
    "react": "React-Dark", "nodejs": "NodeJS-Dark", "django": "Django",
    "aws": "AWS-Dark", "gcp": "GCP-Dark", "postgresql": "PostgreSQL-Dark", "mysql": "MySQL-Dark",
    "github": "Github-Dark",
}

# nombre local -> (slug en simple-icons, color del logo[, versión si ya no está en la actual])
SIMPLE_ICONS = {
    "langchain": ("langchain", "#ffffff"),
    "claude": ("claude", "#D97757"),
    "openai": ("openai", "#ffffff"),
    "gemini": ("googlegemini", "#8E75B2"),
    "huggingface": ("huggingface", "#FFD21E"),
    "posthog": ("posthog", "#F9BD2B"),
    "selenium": ("selenium", "#43B02A"),
    "expo": ("expo", "#ffffff"),
    "git": ("git", "#F05032"),
    "n8n": ("n8n", "#EA4B71"),
    "powerautomate": ("powerautomate", "#0066FF", "9.0.0"),
}

TILE = """<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256" fill="none">
<rect width="256" height="256" rx="60" fill="#242938"/>
<g transform="translate(56 56) scale(6)"><path d="{d}" fill="{color}"/></g>
</svg>
"""


def get(url):
    return urllib.request.urlopen(url, timeout=30).read().decode("utf-8")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, file in SKILL_ICONS.items():
        svg = get(SKILL.format(file))
        assert "<script" not in svg.lower()
        (OUT / f"{name}.svg").write_text(svg, encoding="utf-8")
        print("skill ", name)
    for name, (slug, color, *ver) in SIMPLE_ICONS.items():
        d = re.search(r'<path d="([^"]+)"', get(SIMPLE.format(ver[0] if ver else "13.21.0", slug))).group(1)
        (OUT / f"{name}.svg").write_text(TILE.format(d=d, color=color), encoding="utf-8")
        print("simple", name)


if __name__ == "__main__":
    main()
