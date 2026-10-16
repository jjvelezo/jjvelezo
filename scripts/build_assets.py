"""Genera los SVG animados del perfil en assets/.

    whoami.svg   -> ventana con logros destacados + about-me.yml
    bocati.svg   -> tarjeta destacada de Bocati

Uso:  python scripts/build_assets.py
"""
import base64
import io
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

MONO = "'JetBrains Mono','SFMono-Regular',Consolas,Menlo,monospace"
SANS = "'Segoe UI',Inter,Helvetica,Arial,sans-serif"

BG = "#0d1117"
PANEL = "#111722"
BORDER = "#253042"
MUTED = "#5f6f85"
TEXT = "#e6edf3"
SOFT = "#9fb0c3"
CORAL = "#ff7b72"      # guiño al rojo de Bocati
PEACH = "#ffa198"
PURPLE = "#d2a8ff"
BLUE = "#a5d6ff"
ORANGE = "#ffa657"
GREEN = "#7ee787"

# ---------------------------------------------------------------- whoami.svg

HIGHLIGHTS = [
    # cifra, línea 1, línea 2
    ("1st/70", "Won Bancolombia's AI agent challenge", "70 participants from 4 countries"),
    ("−80%", "Process time cut with an AI agent", "40h → 8h on a Bancolombia workflow"),
    ("900+", "Users on Bocati, my startup", "plus 26 partner businesses in Medellín"),
]

ABOUT = [
    ("name", "Juan José Vélez"),
    ("role", "AI & Automation Engineer"),
    ("building", "Bocati — an app against food waste"),
    ("led", "AI adoption for SMEs · gov-backed program"),
    ("focus", "AI agents · automation · full-stack"),
    ("based in", "Medellín, Colombia"),
    ("speaks", "Spanish · English · Italian"),
    ("status", "open to new opportunities"),
]


def whoami_svg():
    W, H = 960, 330

    hl = []
    for i, (big, l1, l2) in enumerate(HIGHLIGHTS):
        y = 132 + i * 62
        hl.append(
            f'<g class="ln" style="animation-delay:{0.2 + i * 0.2:.2f}s">'
            f'<text x="48" y="{y + 9}" fill="{CORAL}" style="font-family:{SANS};font-size:28px;font-weight:800">{escape(big)}</text>'
            f'<text x="170" y="{y - 2}" fill="{TEXT}" style="font-size:12.5px">{escape(l1)}</text>'
            f'<text x="170" y="{y + 16}" fill="{MUTED}" style="font-size:11.5px">{escape(l2)}</text></g>'
        )

    lines, y0, lh = [], 130, 23
    for i, (key, val) in enumerate(ABOUT):
        y = y0 + i * lh
        color = GREEN if key == "status" else TEXT
        v = escape(val).replace(" · ", f' <tspan fill="{MUTED}">·</tspan> ')
        lines.append(
            f'<g class="ln" style="animation-delay:{0.3 + i * 0.1:.2f}s">'
            f'<text x="512" y="{y}" fill="{MUTED}" text-anchor="end">{i + 1}</text>'
            f'<text x="528" y="{y}" xml:space="preserve"><tspan fill="{CORAL}">{escape(key)}:</tspan> <tspan fill="{color}">{v}</tspan></text></g>'
        )
    last_y = y0 + (len(ABOUT) - 1) * lh
    cur_x = 528 + (len(ABOUT[-1][0]) + 2 + len(ABOUT[-1][1])) * 8.1 + 6

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Juan José Vélez — AI &amp; Automation Engineer, founder of Bocati">
<style>
  text {{ font-family: {MONO}; font-size: 14px; }}
  .ln {{ animation: in .5s ease-out both; }}
  .cur {{ animation: blink 1s steps(1) infinite; }}
  @keyframes in {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
</style>
<rect x="8" y="8" width="{W-16}" height="{H-16}" rx="14" fill="{BG}" stroke="{BORDER}"/>
<circle cx="34" cy="34" r="5.5" fill="#ff5f57"/><circle cx="52" cy="34" r="5.5" fill="#febc2e"/><circle cx="70" cy="34" r="5.5" fill="#28c840"/>
<text x="{W/2}" y="38" fill="{MUTED}" style="font-size:12px" text-anchor="middle">~/jjvelezo</text>
<line x1="8" y1="56" x2="{W-8}" y2="56" stroke="{BORDER}"/>

<rect x="28" y="72" width="436" height="234" rx="8" fill="{PANEL}" stroke="{BORDER}"/>
<text x="46" y="96" fill="{SOFT}" style="font-size:11px" font-weight="700" letter-spacing="1.5">HIGHLIGHTS</text>
{chr(10).join(hl)}

<rect x="480" y="72" width="452" height="234" rx="8" fill="{PANEL}" stroke="{BORDER}"/>
<text x="498" y="96" fill="{SOFT}" style="font-size:11px" font-weight="700" letter-spacing="1.5">ABOUT-ME.YML</text>
{chr(10).join(lines)}
<rect class="cur" x="{cur_x:.0f}" y="{last_y - 12}" width="8" height="16" fill="{CORAL}"/>
</svg>
'''


# ---------------------------------------------------------------- bocati.svg


def logo_data_uri(size=240):
    logo = Image.open(ASSETS / "bocati-logo.png").convert("RGBA")
    logo.thumbnail((size, size))
    buf = io.BytesIO()
    logo.save(buf, "PNG", optimize=True)
    return logo.size, "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def bocati_svg():
    (lw, lh), uri = logo_data_uri()
    box = 196
    scale = 150 / max(lw, lh)
    iw, ih = lw * scale, lh * scale
    ix, iy = 32 + (box - iw) / 2, 32 + (box - ih) / 2

    chips, x = [], 264
    for value, label in [("26", "partner businesses"), ("900+", "users"), ("iOS · Android", "live on both stores")]:
        w = 160
        chips.append(
            f'<g transform="translate({x:.0f} 160)"><rect width="{w:.0f}" height="52" rx="10" fill="#ffffff" fill-opacity=".05" stroke="#ffffff" stroke-opacity=".10"/>'
            f'<text x="{w/2:.0f}" y="23" fill="#ffffff" font-weight="800" font-size="17" text-anchor="middle">{value}</text>'
            f'<text x="{w/2:.0f}" y="41" fill="#c9a5a2" font-size="11" text-anchor="middle">{label}</text></g>'
        )
        x += w + 10

    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="960" height="260" viewBox="0 0 960 260" role="img" aria-label="Bocati — anti food-waste app">
<style>
  text {{ font-family: {SANS}; }}
  .pulse {{ animation: pulse 1.8s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }}
  .rise {{ animation: rise .7s ease-out both; }}
  @keyframes pulse {{ 0%,100% {{ opacity: 1; transform: scale(1); }} 50% {{ opacity: .35; transform: scale(1.6); }} }}
  @keyframes rise {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: none; }} }}
</style>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#2a0708"/><stop offset=".55" stop-color="#14090c"/><stop offset="1" stop-color="#0d1117"/>
  </linearGradient>
</defs>
<rect x="1" y="1" width="958" height="258" rx="16" fill="url(#bg)" stroke="#5a1416"/>
<rect x="32" y="32" width="{box}" height="{box}" rx="18" fill="#fff6ee"/>
<image x="{ix:.1f}" y="{iy:.1f}" width="{iw:.1f}" height="{ih:.1f}" href="{uri}" xlink:href="{uri}"/>
<g class="rise">
  <text x="264" y="90" fill="#ffffff" font-size="40" font-weight="800">Bocati</text>
  <text x="264" y="120" fill="#e7cfcc" font-size="15">A marketplace that connects restaurants and cafés with people who want good food</text>
  <text x="264" y="140" fill="#e7cfcc" font-size="15">at a discount — before it goes to waste. Built it full-stack, then went out and sold it.</text>
</g>
{chr(10).join(chips)}
</svg>
'''

# ---------------------------------------------------------------- badges de tiendas

STORE = """<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="56" viewBox="0 0 {w} 56" role="img" aria-label="{small} {big}">
<rect x=".5" y=".5" width="{w1}" height="55" rx="10" fill="#000" stroke="#a6a6a6"/>
<g transform="translate(14 13) scale(1.25)"><path d="{d}" fill="#fff"/></g>
<text x="56" y="23" fill="#fff" font-family="{font}" font-size="{ss}">{small}</text>
<text x="55" y="44" fill="#fff" font-family="{font}" font-size="21" font-weight="600">{big}</text>
</svg>
"""


def store_badge(slug, small, big, w, ss):
    import urllib.request
    svg = urllib.request.urlopen(f"https://cdn.jsdelivr.net/npm/simple-icons@13.21.0/icons/{slug}.svg", timeout=30).read().decode()
    d = svg.split('<path d="')[1].split('"')[0]
    return STORE.format(w=w, w1=w - 1, d=d, small=small, big=big, font=SANS, ss=ss)


def main():
    (ASSETS / "appstore.svg").write_text(store_badge("apple", "Download on the", "App Store", 170, 11), encoding="utf-8")
    (ASSETS / "googleplay.svg").write_text(store_badge("googleplay", "GET IT ON", "Google Play", 186, 10), encoding="utf-8")
    for name, fn in [("whoami.svg", whoami_svg), ("bocati.svg", bocati_svg)]:
        (ASSETS / name).write_text(fn(), encoding="utf-8")
        print("ok", ASSETS / name)


if __name__ == "__main__":
    main()
