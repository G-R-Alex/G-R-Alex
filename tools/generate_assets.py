#!/usr/bin/env python3
"""Génère les SVG animés du README de profil — DA « sport auto » : noir / orange, formes obliques."""
import os
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "assets"
os.makedirs(OUT, exist_ok=True)

# --- palette --------------------------------------------------------------
BG = "#0d1117"        # = fond du thème sombre GitHub, pour que la bannière s'y fonde
PANEL = "#121419"
PANEL2 = "#0f1115"
LINE = "#23262c"
TEXT = "#f4f4f5"
MUTED = "#9ba1a9"
DIM = "#626973"
DARK = "#0a0a0c"
ACCENT = "#ff9b21"    # orange
ACCENT2 = "#f0630b"   # orange profond (dégradés)

SANS = "'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
HEAD = "'Arial Black', 'Segoe UI Black', 'Helvetica Neue', Arial, sans-serif"
MONO = "'JetBrains Mono', 'Fira Code', 'SF Mono', Consolas, 'DejaVu Sans Mono', monospace"

NOMOTION = "@media (prefers-reduced-motion: reduce){*{animation:none !important}}"
OG = (
    f'<linearGradient id="og" x1="0" y1="0" x2="1" y2="0">'
    f'<stop offset="0" stop-color="#ffb63d"/><stop offset="1" stop-color="{ACCENT2}"/></linearGradient>'
)


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def write(name: str, content: str) -> None:
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)
    print("écrit", name, len(content), "octets")


# ---------------------------------------------------------------------------
# 1. BANNIÈRE
# ---------------------------------------------------------------------------
def banner() -> None:
    W, H = 1200, 320
    GROUND = 262
    S = 1.3
    DUR = 9.5
    DRIVE_END = 0.36
    REAR = 46 * S
    FRONT = 212 * S
    CAR_BASE = round(1150 - FRONT)
    CAR_START = -round(FRONT + 40)
    CAR_END = CAR_BASE      # la voiture s'arrête à sa place finale
    TRAVEL = CAR_END - CAR_START
    t0 = CAR_START - CAR_BASE
    t1 = CAR_END - CAR_BASE
    trail_x0 = CAR_START + REAR
    trail_base_w = CAR_BASE + REAR - trail_x0
    trail_end_scale = TRAVEL / trail_base_w
    COVER_BASE = W + 80
    c0 = CAR_START + FRONT - COVER_BASE
    c1 = CAR_END + FRONT - COVER_BASE
    SETTLE = DRIVE_END + 0.12   # le rideau finit de dégager le décor une fois la voiture arrêtée

    def pct(x):
        return f"{x * 100:.2f}%"

    EASE = "cubic-bezier(.2,.65,.3,1)"
    css = f"""
    .car   {{ animation: drive {DUR}s {EASE} infinite; }}
    .cover {{ animation: sweep {DUR}s {EASE} infinite; }}
    .trail {{ animation: grow  {DUR}s {EASE} infinite; transform-box: fill-box; transform-origin: 0 50%; }}
    .fade  {{ animation: fade  {DUR}s linear infinite; }}
    .spin  {{ animation: spin .42s linear infinite; transform-box: fill-box; transform-origin: center; }}
    .pulse {{ animation: pulse 2.4s ease-in-out infinite; }}
    @keyframes drive {{ 0% {{ transform: translateX({t0}px); }} {pct(DRIVE_END)}, 100% {{ transform: translateX({t1}px); }} }}
    @keyframes sweep {{ 0% {{ transform: translateX({c0:.1f}px); }} {pct(DRIVE_END)} {{ transform: translateX({c1:.1f}px); }} {pct(SETTLE)}, 100% {{ transform: translateX(0); }} }}
    @keyframes grow  {{ 0% {{ transform: scaleX(0); }} {pct(DRIVE_END)}, 100% {{ transform: scaleX({trail_end_scale:.5f}); }} }}
    @keyframes fade  {{ 0%, 72% {{ opacity: 1; }} 88%, 100% {{ opacity: 0; }} }}
    @keyframes spin  {{ to {{ transform: rotate(360deg); }} }}
    @keyframes pulse {{ 0%,100% {{ opacity: .35; }} 50% {{ opacity: 1; }} }}
    {NOMOTION}
    """

    wheel = lambda cx: f"""
        <g transform="translate({cx} -14)">
          <circle r="14" fill="#06090d" stroke="#aeb8c2" stroke-width="1.5"/>
          <circle r="9" fill="#141b23" stroke="{ACCENT}" stroke-width="1"/>
          <g class="spin">
            <path d="M0,-8 L0,8 M-7.6,-2.5 L7.6,2.5 M-4.7,6.5 L4.7,-6.5 M-7.6,2.5 L7.6,-2.5 M-4.7,-6.5 L4.7,6.5" stroke="{ACCENT}" stroke-opacity=".75" stroke-width="1"/>
          </g>
          <circle r="2.2" fill="{ACCENT}"/>
        </g>"""

    car = f"""
      <g transform="scale({S})">
        <g opacity=".6">
          <rect x="-78" y="-38" width="68" height="1.2" fill="url(#streak)"/>
          <rect x="-52" y="-27" width="42" height="1.2" fill="url(#streak)"/>
          <rect x="-92" y="-17" width="82" height="1.2" fill="url(#streak)"/>
        </g>
        <ellipse cx="108" cy="1.5" rx="108" ry="3.4" fill="#000" opacity=".6"/>
        <path d="M16,-37 L16,-28.5 M31,-37 L31,-29" stroke="{ACCENT}" stroke-opacity=".7" stroke-width="1.6"/>
        <path d="M-4,-49 L44,-48 L40,-36.5 L1,-37.5 Z" fill="url(#body)" stroke="{ACCENT}" stroke-width="1.2" stroke-linejoin="round"/>
        <path d="M-2,-45.5 L42,-44.5" stroke="{ACCENT}" stroke-opacity=".45" stroke-width="1"/>
        <path d="M8,-9 L5,-21 C5,-25.5 12,-27.5 22,-28.5 L70,-32.5 C84,-34.5 96,-41.5 111,-43.5 C125,-45 137,-44 145,-39.5 L161,-31.5 C173,-28.5 187,-26.5 199,-23.5 C206,-21.5 208,-18.5 207,-14 L206,-9 Z"
              fill="url(#body)" stroke="{ACCENT}" stroke-width="1.3" stroke-linejoin="round"/>
        <path d="M115,-42.2 C127,-43.6 137,-43 142,-39.3 L150,-33.2 L112,-33.2 Z" fill="{ACCENT}" opacity=".18"/>
        <path d="M112,-33.2 L152,-33.2" stroke="{ACCENT}" stroke-opacity=".4" stroke-width="1"/>
        <path d="M84,-29.5 L100,-27.5 M84,-25.5 L100,-23.5" stroke="{ACCENT}" stroke-opacity=".5" stroke-width="1.2" stroke-linecap="round"/>
        <path d="M18,-14.5 C80,-15.5 150,-15 204,-14" stroke="{ACCENT}" stroke-opacity=".6" stroke-width="1.4" fill="none"/>
        <circle cx="128" cy="-24.5" r="7" fill="none" stroke="#f4f4f5" stroke-opacity=".8" stroke-width="1"/>
        <text x="128" y="-21.4" text-anchor="middle" font-family="{MONO}" font-size="8.5" font-weight="700" fill="#f4f4f5" fill-opacity=".9">07</text>
        <rect x="4" y="-23" width="4" height="3.4" rx="1.2" fill="{ACCENT}" class="pulse"/>
        <path d="M195,-25 L206,-21.5 L206,-19.5 L192,-22.6 Z" fill="#fff" opacity=".92"/>
        <path d="M184,-8.2 L214,-8.2" stroke="{ACCENT}" stroke-width="2" stroke-linecap="round"/>
        <path d="M28,-14 A18,18 0 0 1 64,-14 Z" fill="{BG}"/>
        <path d="M134,-14 A18,18 0 0 1 170,-14 Z" fill="{BG}"/>{wheel(46)}{wheel(152)}
      </g>"""

    ticks = "".join(
        f'<polygon points="{x + 8},{GROUND + 12} {x + 34},{GROUND + 12} {x + 30},{GROUND + 14.4} {x + 4},{GROUND + 14.4}" fill="#2a2e36"/>'
        for x in range(0, W, 70)
    )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Alex Goncalves Rodrigues, développeur et étudiant en cybersécurité. Une voiture de course traverse la bannière en laissant des traces orange.">
  <title>Alex Goncalves Rodrigues</title>
  <defs>
    <style>{css}</style>
    {OG}
    <linearGradient id="wedge" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#171a21"/><stop offset="1" stop-color="{BG}"/>
    </linearGradient>
    <linearGradient id="body" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#22262e"/><stop offset="1" stop-color="#101319"/>
    </linearGradient>
    <linearGradient id="streak" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{ACCENT}" stop-opacity="0"/><stop offset="1" stop-color="{ACCENT}" stop-opacity=".9"/>
    </linearGradient>
    <filter id="glow" x="-5%" y="-300%" width="110%" height="700%"><feGaussianBlur stdDeviation="3.4"/></filter>
  </defs>

  <rect width="{W}" height="{H}" rx="16" fill="{BG}"/>

  <!-- décor et texte : révélés par le passage de la voiture -->
  <g class="fade">
    <polygon points="782,0 {W},0 {W},{H} 662,{H}" fill="url(#wedge)"/>
    <polygon points="760,0 784,0 664,{H} 640,{H}" fill="url(#og)"/>
    <polygon points="808,0 816,0 696,{H} 688,{H}" fill="#fff" opacity=".4"/>
    <polygon points="834,0 838,0 718,{H} 714,{H}" fill="url(#og)" opacity=".6"/>
    <g transform="translate(96 0) skewX(-10)">
      <text x="0" y="116" font-family="{HEAD}" font-size="92" font-weight="900" letter-spacing="2" fill="{TEXT}">ALEX</text>
      <text x="0" y="158" font-family="{HEAD}" font-size="29" font-weight="900" letter-spacing="5" fill="url(#og)">GONCALVES RODRIGUES</text>
      <text x="2" y="190" font-family="{MONO}" font-size="14" letter-spacing="3" fill="{MUTED}">DÉVELOPPEUR / CYBERSÉCURITÉ / MSC EPITECH</text>
    </g>
  </g>
  <rect class="cover" x="{COVER_BASE}" y="0" width="2600" height="{H}" fill="{BG}"/>

  <!-- route et traces de pneus -->
  <rect x="0" y="{GROUND}" width="{W}" height="1.2" fill="#2a2e36"/>
  {ticks}
  <g class="fade">
    <rect class="trail" x="{trail_x0:.1f}" y="{GROUND - 3}" width="{trail_base_w}" height="6" fill="{ACCENT}" opacity=".6" filter="url(#glow)"/>
    <rect class="trail" x="{trail_x0:.1f}" y="{GROUND - 1.4}" width="{trail_base_w}" height="2.2" rx="1" fill="{ACCENT}" opacity=".95"/>
    <rect class="trail" x="{trail_x0:.1f}" y="{GROUND + 3.2}" width="{trail_base_w}" height="1.2" rx=".6" fill="{ACCENT2}" opacity=".6"/>
  </g>

  <g transform="translate({CAR_BASE} {GROUND})">
    <g class="fade"><g class="car">{car}
    </g></g>
  </g>
</svg>
"""
    write("banner.svg", svg)


# ---------------------------------------------------------------------------
# 2. TERMINAL
# ---------------------------------------------------------------------------
def terminal() -> None:
    W, H = 860, 290
    DUR = 15.0
    FS = 16
    CW = FS * 0.6
    X0 = 30
    LH = 30
    Y0 = 90

    def pct(t):
        return f"{t / DUR * 100:.2f}%"

    lines = [
        ("whoami", "cmd", 0.4, 1.3),
        ("alex — étudiant MSc @ Epitech", "out", 1.6, 2.4),
        ("cat stack.txt", "cmd", 3.0, 4.1),
        ("php  laravel  java  python  godot  docker  git  linux", "out", 4.4, 5.3),
        ("./focus --now", "cmd", 6.0, 7.0),
        ("cybersécurité · devsecops", "out", 7.3, 8.3),
    ]
    FADE_START, FADE_END = 13.0, 14.0

    css = [
        f".tfade {{ animation: tfade {DUR}s linear infinite; }}",
        ".blink { animation: blink 1.05s steps(1) infinite; }",
        f"@keyframes tfade {{ 0%, {pct(FADE_START)} {{ opacity: 1; }} {pct(FADE_END)}, 100% {{ opacity: 0; }} }}",
        "@keyframes blink { 0%,100% { opacity: 1; } 50% { opacity: 0; } }",
        NOMOTION,
    ]
    body = []
    for i, (txt, kind, a, b) in enumerate(lines):
        y = Y0 + i * LH
        n = len(txt)
        prefix = 2 if kind == "cmd" else 0
        x_text = X0 + prefix * CW
        w = n * CW
        total = (n + prefix) * CW
        fill = TEXT if kind == "cmd" else MUTED
        if kind == "cmd":
            body.append(f'<text x="{X0}" y="{y}" font-family="{MONO}" font-size="{FS}" fill="{ACCENT}">$</text>')
        body.append(
            f'<text x="{x_text}" y="{y}" font-family="{MONO}" font-size="{FS}" fill="{fill}" '
            f'textLength="{w:.1f}" lengthAdjust="spacing" xml:space="preserve">{esc(txt)}</text>'
        )
        steps = n + prefix
        timing = f"steps({steps}, end)" if kind == "cmd" else "linear"
        css.append(
            f"@keyframes c{i} {{ 0%, {pct(a)} {{ transform: translateX(0); animation-timing-function: {timing}; }} "
            f"{pct(b)}, 100% {{ transform: translateX({total + 6:.1f}px); }} }}"
        )
        css.append(f".c{i} {{ transform: translateX({total + 6:.1f}px); animation: c{i} {DUR}s infinite; }}")
        css.append(
            f"@keyframes v{i} {{ 0%, {pct(a - 0.05)} {{ opacity: 0; }} {pct(a)}, {pct(b + 0.35)} {{ opacity: 1; }} "
            f"{pct(b + 0.4)}, 100% {{ opacity: 0; }} }}"
        )
        css.append(f".v{i} {{ opacity: 0; animation: v{i} {DUR}s linear infinite; }}")
        cursor = (
            f'<g class="v{i}"><rect class="blink" x="{X0}" y="{y - 15}" width="{CW:.1f}" height="20" fill="{ACCENT}"/></g>'
            if kind == "cmd"
            else ""
        )
        body.append(
            f'<g class="c{i}"><rect x="{X0}" y="{y - 17}" width="{total + 40:.1f}" height="24" fill="{PANEL}"/>{cursor}</g>'
        )

    y_last = Y0 + len(lines) * LH
    css.append(
        f"@keyframes last {{ 0%, {pct(8.9)} {{ opacity: 0; }} {pct(9.0)}, 100% {{ opacity: 1; }} }} .last {{ animation: last {DUR}s linear infinite; }}"
    )
    body.append(
        f'<g class="last"><text x="{X0}" y="{y_last}" font-family="{MONO}" font-size="{FS}" fill="{ACCENT}">$</text>'
        f'<rect class="blink" x="{X0 + 2 * CW}" y="{y_last - 15}" width="{CW:.1f}" height="20" fill="{ACCENT}"/></g>'
    )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Terminal : alex, étudiant MSc à Epitech ; stack php, laravel, java, python, godot, docker, git, linux ; focus cybersécurité, devsecops.">
  <title>Terminal</title>
  <defs>{OG}<style>{chr(10).join(css)}</style></defs>
  <rect width="{W}" height="{H}" rx="14" fill="{PANEL}"/>
  <path d="M0,14 A14,14 0 0 1 14,0 H{W - 14} A14,14 0 0 1 {W},14 V44 H0 Z" fill="{PANEL2}"/>
  <polygon points="26,15 62,15 55,29 19,29" fill="url(#og)"/>
  <polygon points="68,15 78,15 71,29 61,29" fill="#2a2e36"/>
  <polygon points="84,15 90,15 83,29 77,29" fill="#2a2e36"/>
  <text x="{W - 28}" y="27" text-anchor="end" font-family="{MONO}" font-size="12" fill="{DIM}" letter-spacing="1.5">ALEX@G-R-ALEX ~</text>
  <rect y="43" width="{W}" height="2" fill="url(#og)" opacity=".85"/>
  <g class="tfade">
    {chr(10).join(body)}
  </g>
</svg>
"""
    write("terminal.svg", svg)


# ---------------------------------------------------------------------------
# 3. TITRES DE SECTION
# ---------------------------------------------------------------------------
def headers() -> None:
    W, H = 860, 52
    items = [("header-apropos", "À PROPOS"), ("header-stack", "STACK"), ("header-contact", "CONTACT")]
    for fname, label in items:
        tw = len(label) * 19 + 40
        x1 = tw + 30
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{esc(label.title())}">
  <title>{esc(label.title())}</title>
  <defs>{OG}
    <linearGradient id="hl" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".85"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="bar"><polygon points="{x1 + 6},21 {W},21 {W},27 {x1},27"/></clipPath>
    <style>
      .hl {{ animation: hl 4.8s cubic-bezier(.45,0,.25,1) infinite; }}
      @keyframes hl {{ from {{ transform: translateX(-160px); }} 70%, to {{ transform: translateX({W}px); }} }}
      {NOMOTION}
    </style>
  </defs>
  <polygon points="16,6 {16 + tw},6 {tw},50 0,50" fill="url(#og)"/>
  <text transform="translate(34 35) skewX(-17.6)" font-family="{HEAD}" font-size="23" font-weight="900" fill="{DARK}"
        textLength="{len(label) * 19}" lengthAdjust="spacing" xml:space="preserve">{esc(label)}</text>
  <polygon points="{x1 + 6},21 {W},21 {W},27 {x1},27" fill="url(#og)" opacity=".92"/>
  <g clip-path="url(#bar)"><rect class="hl" x="0" y="21" width="160" height="6" fill="url(#hl)"/></g>
  <polygon points="{x1 + 16},33 {W},33 {W},35 {x1 + 12},35" fill="#2a2e36"/>
</svg>
"""
        write(fname + ".svg", svg)


# ---------------------------------------------------------------------------
# 4. SÉPARATEUR « COMPTE-TOURS »
# ---------------------------------------------------------------------------
def divider() -> None:
    W, H = 860, 22
    n = 56
    pitch = (W - 20) / n
    seg = []
    for i in range(n):
        x = 6 + i * pitch
        red = i >= n - 9
        cls = "r" if red else "s"
        base = "#2b1a0e" if red else "#1d2026"
        seg.append(
            f'<polygon class="{cls}" style="animation-delay:{i * 0.07:.2f}s" points="{x + 6:.1f},3 {x + 6 + pitch * .52:.1f},3 {x + pitch * .52:.1f},19 {x:.1f},19" fill="{base}"/>'
        )
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="presentation" aria-hidden="true">
  <defs><style>
    .s {{ animation: rev 5.2s linear infinite; }}
    .r {{ animation: rev2 5.2s linear infinite; }}
    @keyframes rev  {{ 0% {{ fill: #1d2026; }} 5% {{ fill: {ACCENT}; }} 24% {{ fill: #1d2026; }} 100% {{ fill: #1d2026; }} }}
    @keyframes rev2 {{ 0% {{ fill: #2b1a0e; }} 5% {{ fill: #fff; }} 12% {{ fill: {ACCENT2}; }} 30% {{ fill: #2b1a0e; }} 100% {{ fill: #2b1a0e; }} }}
    {NOMOTION}
  </style></defs>
  {''.join(seg)}
</svg>
"""
    write("divider.svg", svg)


# ---------------------------------------------------------------------------
# 5. STACK
# ---------------------------------------------------------------------------
def stack() -> None:
    W = 860
    rows = [
        ("DÉVELOPPEMENT", ["PHP", "Laravel", "Java", "Python", "JavaScript", "HTML / CSS", "Svelte", "SQL"]),
        ("OUTILS", ["Git", "GitHub", "Docker", "Linux", "Bash", "AWS"]),
        ("SÉCURITÉ", ["Sécurité web", "XSS", "DevSecOps · en exploration"]),
    ]
    ROW_H = 76
    H = 24 + ROW_H * len(rows)
    out, idx = [], 0
    css = [
        ".chip { animation: wave 8s ease-in-out infinite; }",
        "@keyframes wave { 0%, 100% { stroke: #2a2e36; fill: " + PANEL + "; } 6% { stroke: " + ACCENT + "; fill: #1c1713; } 14% { stroke: #2a2e36; fill: " + PANEL + "; } }",
        NOMOTION,
    ]
    for r, (label, items) in enumerate(rows):
        y = 18 + r * ROW_H
        out.append(f'<polygon points="6,{y + 2} 13,{y + 2} 9,{y + 14} 2,{y + 14}" fill="url(#og)"/>')
        out.append(f'<text x="22" y="{y + 13}" font-family="{MONO}" font-size="11" letter-spacing="2.4" fill="#8a919a">{label}</text>')
        x = 0
        for it in items:
            w = len(it) * 8.2 + 34
            y0 = y + 26
            out.append(
                f'<polygon class="chip" style="animation-delay:{idx * 0.28:.2f}s" points="{x + 9:.1f},{y0} {x + w + 9:.1f},{y0} {x + w:.1f},{y0 + 34} {x:.1f},{y0 + 34}" fill="{PANEL}" stroke="#2a2e36" stroke-width="1.2" stroke-linejoin="round"/>'
                f'<text x="{x + w / 2 + 4.5:.1f}" y="{y0 + 22.2}" text-anchor="middle" font-family="{SANS}" font-size="14" font-style="italic" font-weight="600" fill="{TEXT}">{esc(it)}</text>'
            )
            x += w + 16
            idx += 1
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Compétences : développement, outils, sécurité">
  <title>Stack et compétences</title>
  <defs>{OG}<style>{chr(10).join(css)}</style></defs>
  {''.join(out)}
</svg>
"""
    write("stack.svg", svg)


# ---------------------------------------------------------------------------
# 6. BOUTON GITHUB
# ---------------------------------------------------------------------------
def button() -> None:
    W, H = 260, 52
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Mon profil GitHub, G-R-Alex">
  <title>GitHub · G-R-Alex</title>
  <defs>{OG}
    <clipPath id="b"><polygon points="14,0 {W},0 {W - 14},{H} 0,{H}"/></clipPath>
    <linearGradient id="sh" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
    <style>
      .sh {{ animation: sh 3.6s ease-in-out infinite; }}
      @keyframes sh {{ 0% {{ transform: translateX(0); }} 55%, 100% {{ transform: translateX(380px); }} }}
      {NOMOTION}
    </style>
  </defs>
  <polygon points="14,0 {W},0 {W - 14},{H} 0,{H}" fill="url(#og)"/>
  <g clip-path="url(#b)"><g transform="skewX(-20)"><rect class="sh" x="-120" y="0" width="70" height="{H}" fill="url(#sh)"/></g></g>
  <text transform="translate({W / 2 + 4} 32) skewX(-14)" text-anchor="middle" font-family="{HEAD}" font-size="17" font-weight="900" letter-spacing="2" fill="{DARK}">GITHUB  ›  G-R-ALEX</text>
</svg>
"""
    write("btn-github.svg", svg)


if __name__ == "__main__":
    banner()
    terminal()
    headers()
    divider()
    stack()
    button()
