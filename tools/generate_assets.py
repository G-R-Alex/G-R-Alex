#!/usr/bin/env python3
"""Génère les SVG animés du README de profil (style sobre et élégant, un seul accent)."""
import os
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "assets"
os.makedirs(OUT, exist_ok=True)

BG = "#0d1117"
PANEL = "#0f151c"
LINE = "#1f2933"
TEXT = "#e6edf3"
MUTED = "#8b98a5"
DIM = "#5b6772"
ACCENT = "#5ad1b5"

SANS = "Inter, 'Segoe UI', 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif"
MONO = "'JetBrains Mono', 'Fira Code', 'SF Mono', Consolas, 'DejaVu Sans Mono', monospace"

NOMOTION = "@media (prefers-reduced-motion: reduce){*{animation:none !important}}"


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def write(name: str, content: str) -> None:
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)
    print("écrit", name, len(content), "octets")


# ---------------------------------------------------------------------------
# 1. BANNIÈRE : une voiture traverse l'écran, laisse des traces et révèle le texte
# ---------------------------------------------------------------------------
def banner() -> None:
    W, H = 1200, 300
    GROUND = 258
    S = 1.3              # échelle de la voiture
    DUR = 9.5            # durée de la boucle (s)
    DRIVE_END = 0.42     # fin du trajet (part de la boucle)
    REAR = 46 * S        # contact de la roue arrière
    FRONT = 212 * S      # nez de la voiture (splitter compris)
    CAR_BASE = round(1135 - FRONT)   # position "statique" de la voiture (si pas d'animation)
    CAR_START = -round(FRONT + 40)   # départ (hors cadre à gauche)
    CAR_END = 1260                   # arrivée (hors cadre à droite)
    TRAVEL = CAR_END - CAR_START

    t0 = CAR_START - CAR_BASE                  # translateX de départ
    t1 = CAR_END - CAR_BASE                    # translateX d'arrivée
    trail_x0 = CAR_START + REAR                # début de la trace
    trail_base_w = CAR_BASE + REAR - trail_x0  # largeur de la trace en état statique
    trail_end_scale = TRAVEL / trail_base_w
    cover_x = CAR_BASE + FRONT                 # bord gauche du rideau (état statique)

    def pct(x):
        return f"{x * 100:.2f}%"

    css = f"""
    .car   {{ animation: drive {DUR}s cubic-bezier(.32,.12,.38,1) infinite; }}
    .cover {{ animation: drive {DUR}s cubic-bezier(.32,.12,.38,1) infinite; }}
    .trail {{ animation: grow  {DUR}s cubic-bezier(.32,.12,.38,1) infinite; transform-box: fill-box; transform-origin: 0 50%; }}
    .fade  {{ animation: fade  {DUR}s linear infinite; }}
    .spin  {{ animation: spin .42s linear infinite; transform-box: fill-box; transform-origin: center; }}
    .pulse {{ animation: pulse 2.4s ease-in-out infinite; }}
    @keyframes drive {{
      0%   {{ transform: translateX({t0}px); }}
      {pct(DRIVE_END)} {{ transform: translateX({t1}px); }}
      100% {{ transform: translateX({t1}px); }}
    }}
    @keyframes grow {{
      0%   {{ transform: scaleX(0); }}
      {pct(DRIVE_END)} {{ transform: scaleX({trail_end_scale:.5f}); }}
      100% {{ transform: scaleX({trail_end_scale:.5f}); }}
    }}
    @keyframes fade {{
      0%, 72% {{ opacity: 1; }}
      88%, 100% {{ opacity: 0; }}
    }}
    @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
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
        <!-- traînées de vitesse -->
        <g opacity=".55">
          <rect x="-78" y="-38" width="68" height="1.2" fill="url(#streak)"/>
          <rect x="-52" y="-27" width="42" height="1.2" fill="url(#streak)"/>
          <rect x="-92" y="-17" width="82" height="1.2" fill="url(#streak)"/>
        </g>
        <ellipse cx="108" cy="1.5" rx="108" ry="3.4" fill="#000" opacity=".55"/>

        <!-- aileron arrière : montants puis plan -->
        <path d="M16,-37 L16,-28.5 M31,-37 L31,-29" stroke="{ACCENT}" stroke-opacity=".7" stroke-width="1.6"/>
        <path d="M-4,-49 L44,-48 L40,-36.5 L1,-37.5 Z" fill="url(#body)" stroke="{ACCENT}" stroke-width="1.2" stroke-linejoin="round"/>
        <path d="M-2,-45.5 L42,-44.5" stroke="{ACCENT}" stroke-opacity=".45" stroke-width="1"/>

        <!-- carrosserie : nez bas, cabine avancée, capot moteur long -->
        <path d="M8,-9 L5,-21 C5,-25.5 12,-27.5 22,-28.5 L70,-32.5 C84,-34.5 96,-41.5 111,-43.5 C125,-45 137,-44 145,-39.5 L161,-31.5 C173,-28.5 187,-26.5 199,-23.5 C206,-21.5 208,-18.5 207,-14 L206,-9 Z"
              fill="url(#body)" stroke="{ACCENT}" stroke-width="1.3" stroke-linejoin="round"/>
        <!-- vitre -->
        <path d="M115,-42.2 C127,-43.6 137,-43 142,-39.3 L150,-33.2 L112,-33.2 Z" fill="{ACCENT}" opacity=".16"/>
        <path d="M112,-33.2 L152,-33.2" stroke="{ACCENT}" stroke-opacity=".4" stroke-width="1"/>
        <!-- prise d'air latérale et ligne de livrée -->
        <path d="M84,-29.5 L100,-27.5 M84,-25.5 L100,-23.5" stroke="{ACCENT}" stroke-opacity=".45" stroke-width="1.2" stroke-linecap="round"/>
        <path d="M18,-14.5 C80,-15.5 150,-15 204,-14" stroke="{ACCENT}" stroke-opacity=".55" stroke-width="1.4" fill="none"/>
        <!-- disque de numéro -->
        <circle cx="128" cy="-24.5" r="7" fill="none" stroke="#e6edf3" stroke-opacity=".8" stroke-width="1"/>
        <text x="128" y="-21.4" text-anchor="middle" font-family="{MONO}" font-size="8.5" font-weight="700" fill="#e6edf3" fill-opacity=".9">07</text>
        <!-- feux, phare, splitter -->
        <rect x="4" y="-23" width="4" height="3.4" rx="1.2" fill="{ACCENT}" class="pulse"/>
        <path d="M195,-25 L206,-21.5 L206,-19.5 L192,-22.6 Z" fill="#fff" opacity=".92"/>
        <path d="M184,-8.2 L214,-8.2" stroke="{ACCENT}" stroke-width="2" stroke-linecap="round"/>
        <!-- passages de roue -->
        <path d="M28,-14 A18,18 0 0 1 64,-14 Z" fill="{BG}"/>
        <path d="M134,-14 A18,18 0 0 1 170,-14 Z" fill="{BG}"/>
        <!-- roues -->{wheel(46)}{wheel(152)}
      </g>"""

    ticks = "".join(
        f'<rect x="{x}" y="{GROUND + 12}" width="26" height="1.2" fill="{LINE}"/>'
        for x in range(10, W, 64)
    )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Alex Goncalves Rodrigues, développeur et étudiant en cybersécurité">
  <title>Alex Goncalves Rodrigues</title>
  <defs>
    <style>{css}</style>
    <linearGradient id="body" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#1d252f"/><stop offset="1" stop-color="#10161d"/>
    </linearGradient>
    <linearGradient id="streak" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{ACCENT}" stop-opacity="0"/><stop offset="1" stop-color="{ACCENT}" stop-opacity=".9"/>
    </linearGradient>
    <filter id="glow" x="-5%" y="-300%" width="110%" height="700%"><feGaussianBlur stdDeviation="3.2"/></filter>
  </defs>

  <rect width="{W}" height="{H}" rx="16" fill="{BG}"/>

  <!-- route -->
  <rect x="0" y="{GROUND}" width="{W}" height="1.2" fill="#232d38"/>
  {ticks}

  <!-- traces de pneus -->
  <g class="fade">
    <rect class="trail" x="{trail_x0:.1f}" y="{GROUND - 3}" width="{trail_base_w}" height="6" fill="{ACCENT}" opacity=".55" filter="url(#glow)"/>
    <rect class="trail" x="{trail_x0:.1f}" y="{GROUND - 1.4}" width="{trail_base_w}" height="2.2" rx="1" fill="{ACCENT}" opacity=".95"/>
    <rect class="trail" x="{trail_x0:.1f}" y="{GROUND + 3.2}" width="{trail_base_w}" height="1.2" rx=".6" fill="{ACCENT}" opacity=".45"/>
  </g>

  <!-- texte (révélé par le passage de la voiture) -->
  <g class="fade">
    <text x="64" y="108" font-family="{SANS}" font-size="54" font-weight="700" letter-spacing="-1" fill="{TEXT}">Alex Goncalves Rodrigues</text>
    <text x="66" y="150" font-family="{SANS}" font-size="21" fill="{MUTED}" letter-spacing=".2">Développeur <tspan fill="{ACCENT}">/</tspan> Cybersécurité <tspan fill="{ACCENT}">/</tspan> MSc à Epitech</text>
    <text x="66" y="180" font-family="{MONO}" font-size="14" fill="{DIM}">apprendre en testant, cassant, recommençant.</text>
  </g>
  <rect class="cover" x="{cover_x:.1f}" y="52" width="2400" height="146" fill="{BG}"/>

  <!-- voiture -->
  <g transform="translate({CAR_BASE} {GROUND})">
    <g class="car">{car}
    </g>
  </g>

  <text x="{W - 40}" y="46" text-anchor="end" font-family="{MONO}" font-size="13" fill="{DIM}" letter-spacing="1.5">AIX-EN-PROVENCE · FR</text>
</svg>
"""
    write("banner.svg", svg)


# ---------------------------------------------------------------------------
# 2. TERMINAL : frappe de commandes
# ---------------------------------------------------------------------------
def terminal() -> None:
    W, H = 860, 290
    DUR = 15.0
    FS = 16
    CW = FS * 0.6       # largeur d'un caractère mono
    X0 = 30
    LH = 30
    Y0 = 90             # ligne de base de la première ligne

    def pct(t):
        return f"{t / DUR * 100:.2f}%"

    lines = [
        # (texte, type, début, fin)
        ("whoami", "cmd", 0.4, 1.3),
        ("alex — étudiant MSc @ Epitech · Aix-en-Provence", "out", 1.6, 2.4),
        ("cat stack.txt", "cmd", 3.0, 4.1),
        ("php  laravel  java  python  godot  docker  git  linux", "out", 4.4, 5.3),
        ("./focus --now", "cmd", 6.0, 7.0),
        ("cybersécurité · devsecops · tryhackme · hack the box", "out", 7.3, 8.3),
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
        total = (n + prefix) * CW          # le rideau couvre aussi l'invite "$ "
        fill = TEXT if kind == "cmd" else MUTED
        if kind == "cmd":
            body.append(f'<text x="{X0}" y="{y}" font-family="{MONO}" font-size="{FS}" fill="{ACCENT}">$</text>')
        body.append(
            f'<text x="{x_text}" y="{y}" font-family="{MONO}" font-size="{FS}" fill="{fill}" '
            f'textLength="{w:.1f}" lengthAdjust="spacing" xml:space="preserve">{esc(txt)}</text>'
        )
        # rideau qui découvre le texte (état de base = tout visible, l'animation le referme)
        steps = n + prefix
        timing = f"steps({steps}, end)" if kind == "cmd" else "linear"
        css.append(
            f"@keyframes c{i} {{ 0%, {pct(a)} {{ transform: translateX(0); animation-timing-function: {timing}; }} "
            f"{pct(b)}, 100% {{ transform: translateX({total + 6:.1f}px); }} }}"
        )
        css.append(f".c{i} {{ transform: translateX({total + 6:.1f}px); animation: c{i} {DUR}s infinite; }}")
        # le curseur n'est visible que pendant la frappe
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

    # invite finale avec curseur clignotant
    y_last = Y0 + len(lines) * LH
    css.append(
        f"@keyframes last {{ 0%, {pct(8.9)} {{ opacity: 0; }} {pct(9.0)}, 100% {{ opacity: 1; }} }} .last {{ animation: last {DUR}s linear infinite; }}"
    )
    body.append(
        f'<g class="last"><text x="{X0}" y="{y_last}" font-family="{MONO}" font-size="{FS}" fill="{ACCENT}">$</text>'
        f'<rect class="blink" x="{X0 + 2 * CW}" y="{y_last - 15}" width="{CW:.1f}" height="20" fill="{ACCENT}"/></g>'
    )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Terminal : whoami, cat stack.txt, focus">
  <title>Terminal</title>
  <defs><style>{chr(10).join(css)}</style></defs>
  <rect width="{W}" height="{H}" rx="14" fill="{PANEL}"/>
  <path d="M0,14 A14,14 0 0 1 14,0 H{W - 14} A14,14 0 0 1 {W},14 V44 H0 Z" fill="#131a22"/>
  <rect y="44" width="{W}" height="1" fill="{LINE}"/>
  <circle cx="28" cy="22" r="5" fill="#2b343e"/><circle cx="48" cy="22" r="5" fill="#2b343e"/><circle cx="68" cy="22" r="5" fill="#2b343e"/>
  <text x="{W / 2}" y="27" text-anchor="middle" font-family="{MONO}" font-size="12.5" fill="{DIM}" letter-spacing=".6">alex@g-r-alex: ~</text>
  <g class="tfade">
    {chr(10).join(body)}
  </g>
</svg>
"""
    write("terminal.svg", svg)


# ---------------------------------------------------------------------------
# 3. CARTES PROJETS : bordure traversée par un reflet lumineux
# ---------------------------------------------------------------------------
def cards() -> None:
    W, H = 420, 176
    items = [
        ("card-security-linter", "security-linter", "Analyse un projet PHP, détecte les failles XSS", "et les corrige automatiquement.", ["PHP", "Composer", "XSS"], "PUBLIC", 0.0),
        ("card-wikivalorant", "WikiValorant", "Wiki non officiel en français : principe du jeu,", "rôles des agents, rangs et cartes.", ["Wiki", "FR"], "PUBLIC", 1.5),
        ("card-slimepocalypse", "Slimepocalypse", "Tower defense coopératif sous Godot 4,", "développé à deux, ambiance ferme et vagues.", ["Godot 4", "Co-op"], "EN COURS", 3.0),
        ("card-time-manager", "Time Manager", "Application de gestion du temps :", "backend + frontend, projet Epitech.", ["Backend", "Frontend", "Epitech"], "EN COURS", 4.5),
    ]
    for fname, title, l1, l2, tags, status, delay in items:
        chips = []
        x = 28
        for t in tags:
            w = len(t) * 7.6 + 20
            chips.append(
                f'<rect x="{x}" y="128" width="{w:.1f}" height="26" rx="13" fill="none" stroke="#2a3541"/>'
                f'<text x="{x + w / 2:.1f}" y="145.2" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{ACCENT}">{esc(t)}</text>'
            )
            x += w + 8
        live = status == "EN COURS"
        badge_w = len(status) * 7.4 + 20 + (14 if live else 0)
        badge_x = W - 28 - badge_w
        dot = f'<circle cx="{badge_x + 15:.1f}" cy="34" r="3" fill="{ACCENT}" class="live"/>' if live else ""
        text_cx = (badge_x + 26 + badge_x + badge_w - 10) / 2 if live else badge_x + badge_w / 2
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Projet {esc(title)}">
  <title>{esc(title)}</title>
  <defs><style>
    .edge {{ animation: edge 7s linear infinite; animation-delay: -{delay}s; }}
    .live {{ animation: live 1.8s ease-in-out infinite; }}
    @keyframes edge {{ to {{ stroke-dashoffset: -1000; }} }}
    @keyframes live {{ 0%,100% {{ opacity: .3; }} 50% {{ opacity: 1; }} }}
    {NOMOTION}
  </style></defs>
  <rect width="{W}" height="{H}" rx="14" fill="{PANEL}"/>
  <rect class="edge" x="1" y="1" width="{W - 2}" height="{H - 2}" rx="13" fill="none" stroke="{ACCENT}" stroke-width="1.6"
        stroke-linecap="round" pathLength="1000" stroke-dasharray="130 870"/>
  <text x="28" y="44" font-family="{SANS}" font-size="22" font-weight="650" fill="{TEXT}">{esc(title)}</text>
  <rect x="{badge_x:.1f}" y="22" width="{badge_w:.1f}" height="24" rx="12" fill="none" stroke="#2a3541"/>
  {dot}
  <text x="{text_cx:.1f}" y="38.4" text-anchor="middle" font-family="{MONO}" font-size="10.5" letter-spacing="1" fill="{MUTED}">{status}</text>
  <text x="28" y="82" font-family="{SANS}" font-size="14.5" fill="{MUTED}">{esc(l1)}</text>
  <text x="28" y="104" font-family="{SANS}" font-size="14.5" fill="{MUTED}">{esc(l2)}</text>
  {''.join(chips)}
</svg>
"""
        write(fname + ".svg", svg)


# ---------------------------------------------------------------------------
# 4. STACK : pastilles dont la bordure s'allume en vague
# ---------------------------------------------------------------------------
def stack() -> None:
    W = 860
    rows = [
        ("DÉVELOPPEMENT", ["PHP", "Laravel", "Java", "Python", "JavaScript", "HTML / CSS", "Godot"]),
        ("OUTILS", ["Git", "GitHub", "Docker", "Linux", "Bash"]),
        ("SÉCURITÉ", ["Sécurité web", "XSS", "TryHackMe", "Hack The Box", "DevSecOps · en exploration"]),
    ]
    ROW_H = 74
    H = 24 + ROW_H * len(rows)
    out, idx = [], 0
    css = [
        ".chip { animation: wave 8s ease-in-out infinite; }",
        "@keyframes wave { 0%, 100% { stroke: #26313d; } 6% { stroke: " + ACCENT + "; } 14% { stroke: #26313d; } }",
        NOMOTION,
    ]
    for r, (label, items) in enumerate(rows):
        y = 18 + r * ROW_H
        out.append(f'<text x="2" y="{y + 12}" font-family="{MONO}" font-size="11" letter-spacing="2" fill="#7c8896">{label}</text>')
        x = 0
        for it in items:
            w = len(it) * 8.0 + 30
            out.append(
                f'<g><rect class="chip" style="animation-delay:{idx * 0.28:.2f}s" x="{x + .5}" y="{y + 24.5}" width="{w:.1f}" height="34" rx="17" fill="{PANEL}" stroke="#26313d"/>'
                f'<text x="{x + w / 2:.1f}" y="{y + 46.2}" text-anchor="middle" font-family="{SANS}" font-size="14" fill="{TEXT}">{esc(it)}</text></g>'
            )
            x += w + 10
            idx += 1
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Compétences : développement, outils, sécurité">
  <title>Stack et compétences</title>
  <defs><style>{chr(10).join(css)}</style></defs>
  {''.join(out)}
</svg>
"""
    write("stack.svg", svg)


# ---------------------------------------------------------------------------
# 5. SÉPARATEUR : un reflet qui glisse sur un filet
# ---------------------------------------------------------------------------
def divider() -> None:
    W, H = 860, 20
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="presentation" aria-hidden="true">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{ACCENT}" stop-opacity="0"/><stop offset=".5" stop-color="{ACCENT}"/><stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/>
    </linearGradient>
    <style>
      .sweep {{ animation: sweep 5.5s cubic-bezier(.45,0,.25,1) infinite; }}
      @keyframes sweep {{ from {{ transform: translateX(-260px); }} to {{ transform: translateX({W}px); }} }}
      {NOMOTION}
    </style>
  </defs>
  <rect y="9.5" width="{W}" height="1" fill="{LINE}"/>
  <rect class="sweep" x="0" y="9" width="260" height="2" fill="url(#g)"/>
</svg>
"""
    write("divider.svg", svg)


if __name__ == "__main__":
    banner()
    terminal()
    cards()
    stack()
    divider()
