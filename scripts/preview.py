"""Genera preview.html con el README renderizado por la API oficial de GitHub (mismo HTML saneado que verás en tu perfil).

Uso:  python scripts/preview.py
"""
import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

TEMPLATE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>jjvelezo · README preview</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.5.1/github-markdown-dark.min.css">
<style>
  body { background:#0d1117; margin:0; padding:32px 16px; }
  .frame { max-width:1012px; margin:0 auto; border:1px solid #30363d; border-radius:6px; }
  .head { padding:10px 16px; border-bottom:1px solid #30363d; color:#e6edf3; font:600 14px ui-monospace,Consolas,monospace; }
  .head span { color:#7d8590; font-weight:400; }
  .markdown-body { padding:32px; }
</style></head>
<body><div class="frame"><div class="head">jjvelezo <span>/</span> README<span>.md</span></div>
<article class="markdown-body">__HTML__</article></div>
</body></html>
"""

readme = (ROOT / "README.md").read_text(encoding="utf-8")
req = urllib.request.Request(
    "https://api.github.com/markdown",
    data=json.dumps({"text": readme, "mode": "gfm"}).encode(),
    headers={"Accept": "application/vnd.github+json", "Content-Type": "application/json"},
)
html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")
# Los assets aún no están en GitHub: apuntarlos a los archivos locales.
html = re.sub(r'(src|href)="[^"]*?(assets/[\w./-]+)"', r'\1="\2"', html)
(ROOT / "preview.html").write_text(TEMPLATE.replace("__HTML__", html), encoding="utf-8")
print(ROOT / "preview.html")
