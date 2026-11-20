"""Build the process infographic (FR and EN) as self-contained HTML.
Usage: python build_infographic.py <out_dir>
All pictograms are inline SVG drawn here; no external images."""
import sys, os

NAVY = "#12305a"; BLUE = "#1d6fb8"; GREEN = "#2e8b57"; ORANGE = "#e8902a"; RED = "#c83b3b"
SAND = "#f6ead2"; VEST = "#c9a463"; SKIN = "#7a4a2e"; GREY = "#8fa3b8"; LIGHT = "#eef3f8"; PURPLE = "#6b4fa0"; TEAL = "#2a8c8c"


# ---------------------------------------------------------------- pictogram helpers
def person(x, y, s=1.0, vest=VEST, shirt=NAVY, tablet=False, hat=False, cap=False, female=False):
    """Simple standing figure; (x, y) = feet centre."""
    h = []
    sc = f'transform="translate({x},{y}) scale({s})"'
    h.append(f'<g {sc}>')
    h.append(f'<rect x="-9" y="-30" width="7" height="30" rx="3" fill="{NAVY}"/><rect x="2" y="-30" width="7" height="30" rx="3" fill="{NAVY}"/>')
    h.append(f'<path d="M-15 -30 Q-16 -62 0 -64 Q16 -62 15 -30 Z" fill="{shirt}"/>')
    h.append(f'<path d="M-13 -32 L-11 -60 Q-6 -63 -3 -62 L-3 -32 Z M13 -32 L11 -60 Q6 -63 3 -62 L3 -32 Z" fill="{vest}"/>')
    h.append(f'<circle cx="0" cy="-75" r="11" fill="{SKIN}"/>')
    if female:
        h.append(f'<path d="M-12 -78 Q0 -94 12 -78 Q10 -88 0 -89 Q-10 -88 -12 -78 Z" fill="#2b1d14"/><circle cx="0" cy="-89" r="6" fill="#2b1d14"/>')
    if hat:
        h.append(f'<path d="M-17 -82 L17 -82 L11 -88 Q0 -96 -11 -88 Z" fill="#6b4a2a"/>')
    if cap:
        h.append(f'<path d="M-11 -80 Q0 -92 11 -80 L18 -79 L11 -77 Z" fill="{BLUE}"/>')
    if tablet:
        h.append(f'<rect x="6" y="-56" width="17" height="23" rx="2" fill="#20262e"/><rect x="8" y="-54" width="13" height="19" rx="1" fill="#9fd0ff"/>')
    h.append('</g>')
    return "".join(h)


def house(x, y, s=1.0, fill="#fff", roof="#9a5b34", stroke="#4a5663", dashed=False, check=None):
    d = ' stroke-dasharray="4 3"' if dashed else ''
    g = [f'<g transform="translate({x},{y}) scale({s})">',
         f'<rect x="-16" y="-20" width="32" height="22" fill="{fill}" stroke="{stroke}" stroke-width="2"{d}/>',
         f'<path d="M-21 -19 L0 -36 L21 -19 Z" fill="{roof}" stroke="{stroke}" stroke-width="2"{d}/>',
         f'<rect x="-5" y="-11" width="10" height="13" fill="{stroke}" opacity=".55"/>']
    if check:
        g.append(badge(14, -34, check))
    g.append('</g>')
    return "".join(g)


def badge(x, y, kind, r=9):
    if kind == "ok":
        return f'<g transform="translate({x},{y})"><circle r="{r}" fill="{GREEN}"/><path d="M-4.5 0 L-1.2 3.6 L5 -3.6" stroke="#fff" stroke-width="2.4" fill="none" stroke-linecap="round"/></g>'
    if kind == "no":
        return f'<g transform="translate({x},{y})"><circle r="{r}" fill="{RED}"/><path d="M-4 -4 L4 4 M4 -4 L-4 4" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/></g>'
    if kind == "clock":
        return f'<g transform="translate({x},{y})"><circle r="{r}" fill="{ORANGE}"/><path d="M0 -5 L0 0 L4 2" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/></g>'
    return ""


def pin(x, y, s=1.0, col=RED):
    return f'<g transform="translate({x},{y}) scale({s})"><path d="M0 0 C-4 -9 -13 -14 -13 -24 A13 13 0 1 1 13 -24 C13 -14 4 -9 0 0 Z" fill="{col}"/><circle cy="-24" r="5" fill="#fff"/></g>'


def tablet(x, y, w, h, inner=""):
    return (f'<g transform="translate({x},{y})"><rect width="{w}" height="{h}" rx="9" fill="#20262e"/>'
            f'<rect x="6" y="8" width="{w-12}" height="{h-16}" rx="3" fill="#fff"/>{inner}</g>')


def ban(x, y, r=17):
    return f'<g transform="translate({x},{y})"><circle r="{r}" fill="none" stroke="{RED}" stroke-width="4"/><path d="M{-r*0.7} {r*0.7} L{r*0.7} {-r*0.7}" stroke="{RED}" stroke-width="4"/></g>'


def arrow(x1, y1, x2, y2, col=NAVY, w=3, dash=False):
    d = ' stroke-dasharray="7 5"' if dash else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{w}"{d} marker-end="url(#ah)"/>'


def svg(inner, h=170):
    return f'<svg viewBox="0 0 400 {h}" class="pic" aria-hidden="true">{DEFS}{inner}</svg>'


DEFS = ('<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">'
        f'<path d="M0 0L10 5L0 10z" fill="{NAVY}"/></marker></defs>')

SEGPOLY = [  # small PSU drawing reused in several scenes (3 x 2 cells)
    ("M0 0 L60 -4 L58 46 L-3 50 Z", "4"), ("M60 -4 L122 2 L120 44 L58 46 Z", "7"), ("M122 2 L180 -2 L184 48 L120 44 Z", "1"),
    ("M-3 50 L58 46 L62 96 L2 100 Z", "6"), ("M58 46 L120 44 L118 98 L62 96 Z", "2"), ("M120 44 L184 48 L180 96 L118 98 Z", "5")]
SEGC = [(29, 23), (90, 21), (151, 22), (30, 73), (89, 71), (150, 71)]


def psu(x, y, s=1.0, hi="1", txt=True, done=()):
    g = [f'<g transform="translate({x},{y}) scale({s})">']
    for (d, n), (cx, cy) in zip(SEGPOLY, SEGC):
        f = "#d8efe1" if n == hi else ("#e3f3e8" if n in done else "#eef1f5")
        g.append(f'<path d="{d}" fill="{f}" stroke="#7d8b99" stroke-width="1.6"/>')
        if txt:
            g.append(f'<circle cx="{cx}" cy="{cy}" r="11" fill="#fff" stroke="{NAVY}" stroke-width="{2.5 if n == hi else 1.5}"/>'
                     f'<text x="{cx}" y="{cy+5}" text-anchor="middle" font-size="14" font-weight="700" fill="{GREEN if n == hi else NAVY}">{n}</text>')
    g.append(f'<path d="M0 0 L60 -4 L122 2 L180 -2 L184 48 L180 96 L118 98 L62 96 L2 100 L-3 50 Z" fill="none" stroke="{NAVY}" stroke-width="3.5"/>')
    g.append('</g>')
    return "".join(g)


# ---------------------------------------------------------------- scenes
def scene(n, L):
    if n == 1:
        inner = psu(16, 22, 0.78, txt=True)
        return svg(
            tablet(18, 8, 180, 120, inner)
            + f'<text x="108" y="150" text-anchor="middle" font-size="13" fill="{NAVY}" font-weight="600">{L["s1a"]}</text>'
            # battery + power bank
            + f'<g transform="translate(222,26)"><rect width="52" height="26" rx="4" fill="none" stroke="{NAVY}" stroke-width="3"/><rect x="52" y="8" width="5" height="10" fill="{NAVY}"/>'
            + "".join(f'<rect x="{5+i*12}" y="5" width="9" height="16" fill="{GREEN}"/>' for i in range(4)) + '</g>'
            + f'<g transform="translate(222,66)"><rect width="56" height="34" rx="6" fill="#3c4652"/><path d="M28 6 L20 19 L28 19 L24 30 L36 14 L28 14 L32 6 Z" fill="#ffd34d"/></g>'
            # clipboard checklist
            + f'<g transform="translate(300,14)"><rect width="84" height="120" rx="6" fill="#d9b98a"/><rect x="8" y="12" width="68" height="102" fill="#fff"/><rect x="26" y="4" width="32" height="14" rx="4" fill="#6b4a2a"/>'
            + "".join(badge(20, 36 + i * 24, "ok", 7) + f'<rect x="32" y="{32+i*24}" width="36" height="7" rx="3" fill="#c9d3de"/>' for i in range(4)) + '</g>')
    if n == 2:
        return svg(
            f'<path d="M0 150 Q80 90 170 120 T400 100 L400 170 L0 170 Z" fill="#e3efd9"/>'
            + f'<path d="M20 165 C90 120 120 150 190 110" stroke="#b9a27a" stroke-width="14" fill="none" stroke-linecap="round"/>'
            + f'<path d="M20 165 C90 120 120 150 190 110" stroke="#fff" stroke-width="2" stroke-dasharray="8 8" fill="none"/>'
            + f'<path d="M190 30 L300 22 L310 92 L196 100 Z" fill="#dbe8f7" stroke="{NAVY}" stroke-width="3"/>'
            + f'<circle cx="250" cy="62" r="9" fill="{BLUE}" stroke="#fff" stroke-width="3"/>'
            + f'<circle cx="250" cy="62" r="18" fill="{BLUE}" opacity=".18"/>'
            + pin(200, 112, 0.8, RED)
            + f'<text x="200" y="134" font-size="12" fill="{RED}" font-weight="700" text-anchor="middle">{L["s2a"]}</text>'
            + person(318, 160, 1.05, tablet=True, cap=True)
            + person(366, 160, 1.05, vest="#5a3d7a", shirt="#7f5aa8", hat=True)
            + f'<text x="342" y="22" text-anchor="middle" font-size="12" fill="{NAVY}" font-weight="600">{L["s2b"]}</text>')
    if n == 3:
        return svg(
            psu(16, 30, 1.1, hi="1")
            + person(258, 152, 1.1, tablet=True, cap=True)
            + f'<g transform="translate(290,26)"><rect width="104" height="70" rx="8" fill="{LIGHT}" stroke="{NAVY}" stroke-width="2"/>'
            + f'<text x="52" y="27" text-anchor="middle" font-size="11" fill="{NAVY}" font-weight="700">{L["s3a"]}</text>'
            + f'<text x="52" y="50" text-anchor="middle" font-size="22" fill="{GREEN}" font-weight="800">1 → 2 → 3</text></g>'
            + f'<text x="345" y="122" text-anchor="middle" font-size="12" fill="{RED}" font-weight="700">{L["s3b"]}</text>'
            + ban(345, 148, 14))
    if n == 4:
        xs = [40, 115, 190, 265, 340]
        g = f'<path d="M14 58 L372 58 Q392 58 392 80 Q392 104 372 104 L30 104 Q12 104 12 124 Q12 146 34 146 L380 146" fill="none" stroke="{GREEN}" stroke-width="3.5" stroke-dasharray="9 6" marker-end="url(#ah)"/>'
        for i, x in enumerate(xs):
            g += house(x, 54, 0.95, check="ok")
        for i, x in enumerate(xs[::-1]):
            dashed = i == 2
            g += house(x, 140, 0.95, fill="#fff" if not dashed else "#f6f6f6", dashed=dashed, check="ok")
        g += f'<text x="190" y="166" text-anchor="middle" font-size="11" fill="{NAVY}" font-weight="600">{L["s4a"]}</text>'
        return svg(g, 172)
    if n == 5:
        icons = [
            f'<path d="M-13 -8 h26 a5 5 0 0 1 5 5 v10 a5 5 0 0 1 -5 5 h-14 l-8 7 v-7 h-4 a5 5 0 0 1 -5 -5 v-10 a5 5 0 0 1 5 -5z" fill="#fff"/>',
            f'<circle r="7" cy="-6" fill="#fff"/><path d="M-10 12 Q-10 0 0 0 Q10 0 10 12 Z" fill="#fff"/>',
            f'<rect x="-10" y="-13" width="20" height="26" rx="2" fill="#fff"/><path d="M-5 -5h10 M-5 0h10 M-5 5h6" stroke="{NAVY}" stroke-width="2"/>',
            f'<circle r="10" cy="-2" fill="#fff"/><circle r="3" cx="-9" cy="11" fill="#fff"/><text y="3" text-anchor="middle" font-size="12" font-weight="800" fill="{NAVY}">?</text>',
            f'<rect x="-14" y="-10" width="28" height="20" rx="3" fill="#fff"/><path d="M-9 -4h18 M-9 1h18 M-9 6h12" stroke="{NAVY}" stroke-width="1.8"/>',
            f'<rect x="-14" y="-8" width="28" height="19" rx="3" fill="#fff"/><rect x="-6" y="-12" width="12" height="5" fill="#fff"/><circle r="5.5" cy="1" fill="{NAVY}"/>',
            f'<path d="M0 12 C-3 5 -10 1 -10 -5 A10 10 0 1 1 10 -5 C10 1 3 5 0 12Z" fill="#fff"/><circle cy="-5" r="3.5" fill="{NAVY}"/>',
            f'<path d="M-8 4 L0 -6 L8 4 M0 -6 V12" stroke="#fff" stroke-width="3.5" fill="none" stroke-linecap="round"/><path d="M-12 12 h24" stroke="#fff" stroke-width="3"/>',
        ]
        cols = [BLUE, TEAL, PURPLE, ORANGE, GREEN, "#3c4652", RED, NAVY]
        g = ""
        for i, (ic, c) in enumerate(zip(icons, cols)):
            r, cidx = divmod(i, 4)
            x = 52 + cidx * 96; y = 40 + r * 82
            if cidx < 3:
                g += arrow(x + 26, y, x + 64, y, "#9aa8b6", 2.5)
            g += f'<g transform="translate({x},{y})"><circle r="25" fill="{c}"/>{ic}</g>'
            g += f'<text x="{x}" y="{y+40}" text-anchor="middle" font-size="12" font-weight="700" fill="{NAVY}">{i+1}. {L["seq"][i]}</text>'
        g += f'<path d="M340 66 Q392 82 340 96 L64 96 Q30 96 40 112" fill="none" stroke="#9aa8b6" stroke-width="2.5" marker-end="url(#ah)" opacity=".0"/>'
        return svg(g, 172)
    if n == 6:
        g = house(60, 110, 1.35, check="clock")
        g += f'<text x="60" y="150" text-anchor="middle" font-size="12" font-weight="700" fill="{ORANGE}">{L["s6a"]}</text>'
        g += house(190, 110, 1.35, check="no")
        g += f'<g transform="translate(190,58)"><path d="M-9 8 v-18 a3 3 0 0 1 6 0 v8 v-12 a3 3 0 0 1 6 0 v12 v-10 a3 3 0 0 1 6 0 v10 v-6 a3 3 0 0 1 6 0 v14 q0 10 -12 10 h-6 q-8 0 -12 -8 l-6 -10 a3 3 0 0 1 5 -3 z" fill="{RED}"/></g>'
        g += f'<text x="190" y="150" text-anchor="middle" font-size="12" font-weight="700" fill="{RED}">{L["s6b"]}</text>'
        g += house(330, 110, 1.35)
        g += f'<path d="M232 84 Q275 50 304 82" stroke="{NAVY}" stroke-width="3" fill="none" stroke-dasharray="6 5" marker-end="url(#ah)"/>'
        g += ban(268, 60, 15)
        g += f'<text x="330" y="150" text-anchor="middle" font-size="12" font-weight="700" fill="{NAVY}">{L["s6c"]}</text>'
        return svg(g)
    if n == 7:
        g = f'<text x="20" y="28" font-size="13" font-weight="700" fill="{NAVY}">{L["s7a"]}</text>'
        g += f'<rect x="20" y="38" width="170" height="20" rx="10" fill="#e1e7ee"/><rect x="20" y="38" width="170" height="20" rx="10" fill="{GREEN}"/>'
        g += f'<text x="105" y="53" text-anchor="middle" font-size="13" font-weight="800" fill="#fff">5 / 5 ✓</text>'
        for i, x in enumerate([40, 100, 160]):
            g += house(x, 120, 0.9, fill="#d8efe1", check="ok")
        for i, x in enumerate([232, 292]):
            g += house(x, 120, 0.9)
        g += f'<path d="M190 136 L330 136" stroke="{ORANGE}" stroke-width="4" marker-end="url(#ah)"/>'
        g += f'<text x="262" y="158" text-anchor="middle" font-size="12" font-weight="800" fill="{ORANGE}">{L["s7b"]}</text>'
        g += f'<g transform="translate(352,60)"><rect x="0" y="0" width="4" height="80" fill="{NAVY}"/><path d="M4 2 L40 12 L4 24 Z" fill="{GREEN}"/></g>'
        g += f'<text x="360" y="158" text-anchor="middle" font-size="12" font-weight="700" fill="{GREEN}">{L["s7c"]}</text>'
        return svg(g)
    if n == 8:
        rows = [("1", "A", GREEN), ("2", "A", GREEN), ("3", "C", GREEN), ("4", "D", ORANGE)]
        g = f'<g transform="translate(20,12)"><rect width="190" height="146" rx="8" fill="#fff" stroke="{NAVY}" stroke-width="2"/>'
        g += f'<rect width="190" height="28" rx="8" fill="{NAVY}"/><text x="14" y="19" font-size="12" font-weight="700" fill="#fff">{L["s8a"]}</text>'
        for i, (s, c, col) in enumerate(rows):
            y = 52 + i * 26
            g += f'<text x="16" y="{y}" font-size="13" fill="{NAVY}">Segment {s}</text><text x="118" y="{y}" font-size="15" font-weight="800" fill="{col}">{c}</text>{badge(160, y-5, "ok", 8)}'
        g += '</g>'
        g += psu(232, 40, 0.85, hi="", txt=True, done=("4", "7", "1", "6"))
        g += f'<text x="310" y="150" text-anchor="middle" font-size="12" font-weight="700" fill="{NAVY}">{L["s8b"]}</text>'
        return svg(g)
    if n == 9:
        g = person(36, 132, 0.95, tablet=True, cap=True)
        g += arrow(58, 90, 88, 90)
        g += person(112, 132, 0.95, vest="#2f6fb0", tablet=True)
        g += arrow(134, 90, 164, 90)
        g += person(188, 132, 0.95, vest="#1d4a85", shirt="#28333f", tablet=True)
        g += arrow(210, 90, 240, 90)
        g += f'<g transform="translate(244,56)"><rect width="46" height="62" rx="5" fill="#3c4652"/>' + "".join(f'<rect x="7" y="{8+i*17}" width="32" height="11" rx="2" fill="#5b6876"/><circle cx="33" cy="{13+i*17}" r="2.5" fill="#7fe08a"/>' for i in range(3)) + '</g>'
        g += arrow(292, 90, 318, 90)
        g += f'<g transform="translate(322,56)"><rect width="66" height="44" rx="4" fill="#20262e"/><rect x="5" y="5" width="56" height="34" fill="#dbe8f7"/><path d="M10 32 L22 20 L32 26 L46 12 L56 18" stroke="{BLUE}" stroke-width="2.5" fill="none"/><rect x="-6" y="44" width="78" height="6" rx="2" fill="#3c4652"/></g>'
        g += f'<g transform="translate(374,40)"><circle r="12" fill="none" stroke="{NAVY}" stroke-width="4"/><path d="M8 8 L18 18" stroke="{NAVY}" stroke-width="5" stroke-linecap="round"/></g>'
        for x, t in zip([36, 112, 188, 267, 352], L["s9"]):
            g += f'<text x="{x}" y="154" text-anchor="middle" font-size="10.5" font-weight="700" fill="{NAVY}">{t}</text>'
        return svg(g)
    if n == 10:
        g = f'<g transform="translate(20,22)"><rect width="56" height="96" rx="9" fill="#20262e"/><rect x="5" y="10" width="46" height="74" rx="2" fill="#dbe8f7"/>'
        g += f'<path d="M18 36 q-4 6 0 14 q6 8 14 8 l4 -5 l-7 -6 l-4 3 q-4 -2 -6 -7 l3 -4 l-5 -8 z" fill="{GREEN}"/></g>'
        g += f'<path d="M84 40 q10 10 0 20 M92 34 q16 16 0 32" stroke="{GREEN}" stroke-width="3" fill="none"/>'
        g += f'<text x="48" y="140" text-anchor="middle" font-size="12" font-weight="700" fill="{NAVY}">{L["s10a"]}</text>'
        g += f'<g transform="translate(128,18)"><rect width="140" height="104" rx="6" fill="#6f7f5e"/>'
        g += "".join(f'<rect x="{x}" y="{y}" width="10" height="8" fill="#d9d2c2"/>' for x, y in [(14, 14), (40, 22), (70, 12), (100, 30), (24, 54), (58, 64), (92, 72), (118, 50), (36, 86)])
        g += "".join(f'<circle cx="{x+5}" cy="{y+4}" r="5" fill="none" stroke="#ffd34d" stroke-width="2.5"/>' for x, y in [(14, 14), (40, 22), (70, 12), (100, 30), (58, 64), (118, 50)])
        g += "".join(f'<circle cx="{x+5}" cy="{y+4}" r="7" fill="none" stroke="{RED}" stroke-width="2.5"/>' for x, y in [(24, 54), (92, 72), (36, 86)])
        g += '</g>'
        g += f'<text x="198" y="140" text-anchor="middle" font-size="12" font-weight="700" fill="{NAVY}">{L["s10b"]}</text>'
        g += f'<g transform="translate(290,30)"><rect width="92" height="62" rx="5" fill="#fff8e6" stroke="#b08a3e" stroke-width="2"/>'
        g += "".join(f'<rect x="10" y="{12+i*14}" width="44" height="6" fill="#c9b48a"/><rect x="60" y="{12+i*14}" width="22" height="6" fill="#7d8b99"/>' for i in range(3))
        g += badge(86, 2, "ok", 12) + '</g>'
        g += f'<text x="336" y="140" text-anchor="middle" font-size="12" font-weight="700" fill="{NAVY}">{L["s10c"]}</text>'
        return svg(g)


# ---------------------------------------------------------------- red lines mini icons
def redline_icon(i):
    base = {
        0: psu(-30, -16, 0.33, hi="7", txt=False),
        1: house(0, 10, 0.75, dashed=True),
        2: house(-12, 10, 0.55) + house(14, 10, 0.55),
        3: f'<rect x="-22" y="-6" width="44" height="12" rx="6" fill="{GREEN}"/><path d="M-4 14 L18 14" stroke="{ORANGE}" stroke-width="3"/>',
        4: f'<rect x="-16" y="-11" width="32" height="22" rx="3" fill="#fff8e6" stroke="#b08a3e" stroke-width="2"/><path d="M-10 -4h20 M-10 2h20" stroke="#c9b48a" stroke-width="2"/>',
        5: f'<rect x="-14" y="-16" width="28" height="32" rx="2" fill="#fff" stroke="{NAVY}" stroke-width="2"/><path d="M-8 -8h16 M-8 -2h16 M-8 4h10" stroke="{NAVY}" stroke-width="2"/>',
        6: pin(0, 14, 0.75, BLUE),
        7: f'<rect x="-12" y="-17" width="24" height="34" rx="4" fill="#20262e"/><rect x="-9" y="-12" width="18" height="22" fill="#9fd0ff"/>',
    }[i]
    return f'<svg viewBox="-34 -30 68 60" class="ri">{base}{ban(0, 0, 25)}</svg>'


ROLE_ICON = {
    "enum": person(0, 48, 0.85, tablet=True, cap=True),
    "chief": person(0, 48, 0.85, vest="#2f6fb0", tablet=True),
    "coord": person(0, 48, 0.85, vest="#1d4a85", shirt="#28333f"),
    "dm": f'<g transform="translate(-22,-10)"><rect width="44" height="30" rx="3" fill="#20262e"/><rect x="4" y="4" width="36" height="22" fill="#dbe8f7"/><path d="M8 22 L16 14 L23 18 L34 8" stroke="{BLUE}" stroke-width="2.5" fill="none"/><rect x="-5" y="30" width="54" height="5" rx="2" fill="#3c4652"/></g>',
    "qa": f'<g><circle cx="-4" cy="2" r="14" fill="none" stroke="{NAVY}" stroke-width="5"/><path d="M6 12 L18 24" stroke="{NAVY}" stroke-width="6" stroke-linecap="round"/>{badge(-4, 2, "ok", 8)}</g>',
}


# ---------------------------------------------------------------- text
FR = dict(
    lang="fr",
    title1="Des données de qualité,", title2="un PSU couvert en entier",
    lead="Le parcours d'une fiche, du départ au serveur. Chaque étape suit le protocole Sankuru (SOP-01 et plan DQA V1.0) et laisse une trace vérifiable : un point GPS, une heure, une fiche soumise.",
    slogan="Chaque structure compte.<br>Chaque fiche se vérifie.",
    phases=["AVANT ET À L'ARRIVÉE", "DANS LE SEGMENT", "CLÔTURER LE PSU", "LE JOUR MÊME ET APRÈS"],
    who="Qui",
    s1a="PSU + segments + segment 1", s2a="centroïde", s2b="Autorité locale",
    s3a="Ordre fixé par BGC", s3b="Ne jamais choisir",
    s4a="Une fiche par structure, même vide",
    seq=["Saluer", "Dépister", "Consentir", "Rappel", "Carte", "Photo", "GPS ≤15 m", "Soumettre"],
    s6a="Absent : revenir", s6b="Refus : noter", s6c="Pas de voisin",
    s7a="Quota ≈ 5 entretiens 12–23 mois", s7b="Finir le segment", s7c="Puis arrêter",
    s8a="Disposition des segments", s8b="Code ↔ carte GPS",
    s9=["Enquêteur", "Chef d'équipe", "Superviseur", "Serveur", "Gestion / Qualité"],
    s10a="Contre-appel", s10b="Audit satellite", s10c="Revue cartes",
    steps=[
        ("Préparer la veille", ["Polygones du PSU et des segments visibles sur la carte CAPI ; segment 1 noté sur la fiche d'affectation.",
                                "CAPI à la bonne version, une soumission test passée ; téléphone et batterie externe chargés.",
                                "Consentements en français et en otetela ; sensibilisation confirmée avec l'autorité locale."], "Chef d'équipe, enquêteur"),
        ("Arriver au PSU", ["Le centroïde sert à naviguer : on n'interroge personne en chemin ni au centroïde.",
                            "Le point bleu doit être dans le polygone du PSU. Sinon, on ne commence pas.",
                            "Visite de courtoisie à l'autorité locale avant le premier ménage."], "Enquêteur, chef d'équipe"),
        ("Commencer au segment 1", ["BGC a numéroté les segments au hasard : le segment 1 est un départ aléatoire. Personne ne le choisit.",
                                    "Entrer dans le polygone du segment 1 avant la première structure.",
                                    "Fixer un sens de balayage en serpentin et l'annoncer au chef d'équipe."], "Enquêteur"),
        ("Chaque structure, une fiche", ["Commencer par la structure la plus proche du point d'entrée, puis la suivante sur la ligne.",
                                         "Ne rien sauter : loin, en pente, clôturé ou « sans enfant ».",
                                         "Inoccupé, non résidentiel, zone abandonnée : une fiche avec GPS quand même. C'est la preuve que la zone a été vérifiée."], "Enquêteur"),
        ("La même séquence, partout", ["Rappel du soignant d'abord, ensuite la carte. Saisir toutes les dates visibles.",
                                       "Une alerte de date ? Revérifier sur la carte avant de partir. Si la carte porte cette date, la garder et l'écrire en commentaire.",
                                       "Photo nette de la carte entière ; GPS ≤ 15 m devant la porte ; fiche fermée et soumise sur place."], "Enquêteur"),
        ("Absents, refus, inaccessibles", ["Absent : fiche, puis revisite le jour même ou le lendemain matin. Au plus deux revisites, puis non-contact documenté.",
                                           "Refus : fiche sans données personnelles. Jamais remplacé par le voisin.",
                                           "Inaccessible ou danger : code motif, chef d'équipe et superviseur informés le jour même."], "Enquêteur, superviseur"),
        ("Finir le segment, toujours", ["Quota atteint au milieu du segment ? On finit quand même le segment (Règle 5.1).",
                                        "Déclarer le segment au chef d'équipe : fiches, ménages éligibles, entretiens, absents à revoir.",
                                        "Segment suivant = numéro suivant, retrouvé sur la carte. Ce n'est pas toujours le voisin."], "Enquêteur, chef d'équipe"),
        ("Clôturer le PSU", ["Revenir chez les absents avant de déclarer le PSU complet.",
                             "Un code A à H pour chaque segment, du 1 au plus haut atteint. Le code doit correspondre aux points GPS sur la carte.",
                             "Sauter un segment : le superviseur seul décide. Remplacer un PSU : DQM et PI, PSU de secours de la liste BGC."], "Chef d'équipe, superviseur"),
        ("Revue le jour même", ["Chef d'équipe : 1re revue de chaque fiche (complétude, photo, GPS, segment, PSU).",
                                "Superviseur : 2e revue, saisie comparée à la photo, puis téléversement.",
                                "Gestion puis Qualité des données : alertes A1–A13, questions aux équipes et correction le jour même."], "Toute la chaîne"),
        ("Contrôles indépendants", ["Contre-enquêtes sur au moins 10 % des entretiens (5 % au hasard, 5 % ciblés), par téléphone sous 48 h.",
                                    "Audit de couverture : points GPS sur image satellite ; re-balayage des segments où des structures manquent.",
                                    "Revue de 100 % des cartes avec l'outil HBR ; observation directe de 5–10 % des entretiens."], "Contrôleurs indépendants, DQM"),
    ],
    red_title="Lignes rouges", red_sub="Chacune est détectée dans les données.",
    red=["Choisir ou changer le segment de départ", "Sauter une structure", "Remplacer un ménage absent ou refusant",
         "Quitter un segment à moitié, quota atteint", "Demander la carte avant le rappel", "Remplir une fiche plus tard ou de mémoire",
         "Prendre le GPS de loin ou depuis la route", "Partager un téléphone ou un code PIN"],
    new_title="Nouveau après la revue BGC",
    new=["Une fiche aussi pour les zones vides ou abandonnées, avec GPS.",
         "Le code de disposition doit correspondre à la carte : pas de « A » s'il reste des structures sans fiche.",
         "Formulaire laissé ouvert pour revenir : autorisé. On enregistre la durée active de l'entretien.",
         "Dates d'une même série identiques ou inversées, ou doses du même âge à des dates différentes : revérifier sur la carte.",
         "« Date illisible » ou « coche seulement » : seulement si c'est vrai. Le taux est suivi par enquêteur.",
         "Codes détaillés pour les segments inaccessibles (forêt, eau, insécurité…)."],
    roles_title="Qui fait quoi",
    roles=[("enum", "Enquêteur", "Applique la séquence à chaque structure. Une fiche par structure, soumise sur place."),
           ("chief", "Chef d'équipe et superviseur", "Revoient chaque fiche le jour même. Seul le superviseur autorise un écart d'ordre ou un segment sauté."),
           ("coord", "Coordinateur terrain", "Organise les équipes, les retours et les ré-entretiens ; transmet tout remplacement de PSU."),
           ("dm", "Gestion des données", "Tient la CAPI, les cartes et le tableau de bord ; produit les alertes ; confirme chaque jour les téléversements."),
           ("qa", "Qualité des données", "Revoit les alertes, décide des actions correctives, commande les contre-enquêtes et l'audit de couverture.")],
    foot1="Un doute sur le terrain ? Appelez le superviseur ou le coordinateur avant de quitter le ménage : corriger sur place est facile, corriger après est presque impossible.",
    foot2="Enquête de couverture vaccinale du Sankuru · UNIKIN, Département de médecine tropicale · Novembre 2026",
)

EN = dict(
    lang="en",
    title1="Quality data,", title2="a PSU covered in full",
    lead="The path of one record, from departure to the server. Each step follows the Sankuru protocol (SOP-01 and DQA Plan V1.0) and leaves a trace that can be checked: a GPS point, a time, a submitted record.",
    slogan="Every structure counts.<br>Every record can be checked.",
    phases=["BEFORE AND ON ARRIVAL", "INSIDE THE SEGMENT", "CLOSING THE PSU", "THE SAME DAY AND AFTER"],
    who="Who",
    s1a="PSU + segments + Segment 1", s2a="centroid", s2b="Local authority",
    s3a="Order set by BGC", s3b="Never choose",
    s4a="One record per structure, even an empty one",
    seq=["Greet", "Screen", "Consent", "Recall", "Card", "Photo", "GPS ≤15 m", "Submit"],
    s6a="Absent: return", s6b="Refusal: record", s6c="No neighbour",
    s7a="Quota ≈ 5 interviews, 12–23 months", s7b="Finish the segment", s7c="Then stop",
    s8a="Segment disposition", s8b="Code ↔ GPS map",
    s9=["Enumerator", "Team chief", "Supervisor", "Server", "Data / Quality"],
    s10a="Phone check", s10b="Satellite audit", s10c="Card review",
    steps=[
        ("Prepare the evening before", ["PSU and segment polygons visible on the CAPI map; Segment 1 written on the assignment sheet.",
                                        "CAPI on the right version, a test submission sent; phone and power bank charged.",
                                        "Consent forms in French and Otetela; sensitisation confirmed with the local authority."], "Team chief, enumerator"),
        ("Arrive at the PSU", ["The centroid is for navigation: nobody is interviewed on the way or at the centroid.",
                               "The blue dot must be inside the PSU polygon. If not, do not start.",
                               "Courtesy visit to the local authority before the first household."], "Enumerator, team chief"),
        ("Start in Segment 1", ["BGC numbered the segments at random: Segment 1 is a random start. Nobody chooses it.",
                                "Get inside the Segment 1 polygon before the first structure.",
                                "Fix a serpentine sweep direction and tell the team chief."], "Enumerator"),
        ("Every structure, one record", ["Start with the structure nearest the entry point, then the next one on the line.",
                                         "Skip nothing: far away, uphill, fenced or \"no child here\".",
                                         "Vacant, non-residential or abandoned area: a record with GPS anyway. It proves the area was checked."], "Enumerator"),
        ("The same sequence, everywhere", ["Caregiver recall first, then the card. Enter every visible date.",
                                           "A date prompt? Recheck against the card before leaving. If the card shows that date, keep it and note it in the comment.",
                                           "Clear photo of the whole card; GPS ≤ 15 m at the door; record closed and submitted on the spot."], "Enumerator"),
        ("Absent, refusing, inaccessible", ["Absent: record, then a revisit the same day or next morning. At most two revisits, then a documented non-contact.",
                                            "Refusal: record with no personal data. Never replaced by the neighbour.",
                                            "Inaccessible or unsafe: reason code; team chief and supervisor told the same day."], "Enumerator, supervisor"),
        ("Always finish the segment", ["Quota reached halfway through the segment? Finish the segment anyway (Rule 5.1).",
                                       "Declare the segment to the team chief: records, eligible households, interviews, absent households to revisit.",
                                       "Next segment = next number, found on the map. It is not always the neighbour."], "Enumerator, team chief"),
        ("Close the PSU", ["Return to absent households before declaring the PSU complete.",
                           "A code A to H for every segment from 1 to the highest reached. The code must match the GPS points on the map.",
                           "Skipping a segment: the field supervisor alone decides. Replacing a PSU: DQM and PI, backup PSU from the BGC list."], "Team chief, supervisor"),
        ("Same-day review", ["Team chief: first review of every record (complete, photo, GPS, segment, PSU).",
                             "Field supervisor: second review, entries compared with the photo, then upload.",
                             "Data management, then data quality: alerts A1–A13, queries to the teams, corrected the same day."], "The whole chain"),
        ("Independent checks", ["Back-checks on at least 10% of interviews (5% random, 5% targeted), by phone within 48 hours.",
                                "Coverage audit: GPS points on satellite imagery; re-sweep of segments where structures are missing.",
                                "100% of cards reviewed with the HBR tool; direct observation of 5–10% of interviews."], "Independent back-checkers, DQM"),
    ],
    red_title="Red lines", red_sub="Each one is detected in the data.",
    red=["Choosing or changing the starting segment", "Skipping a structure", "Replacing an absent or refusing household",
         "Leaving a segment half done because the quota is reached", "Asking for the card before recall", "Filling a record later or from memory",
         "Taking GPS from a distance or from the road", "Sharing a phone or a PIN"],
    new_title="New after the BGC review",
    new=["A record for empty or abandoned areas too, with GPS.",
         "The disposition code must match the map: no \"A\" while structures are left without a record.",
         "A form left open to come back later is allowed. The active interview time is recorded.",
         "Doses in one series with the same or reversed dates, or same-age doses on different dates: recheck against the card.",
         "\"Date illegible\" or \"tick only\": only when true. The rate is tracked by enumerator.",
         "Detailed codes for inaccessible segments (forest, water, insecurity…)."],
    roles_title="Who does what",
    roles=[("enum", "Enumerator", "Follows the sequence at every structure. One record per structure, submitted on the spot."),
           ("chief", "Team chief and supervisor", "Review every record the same day. Only the field supervisor authorises an order change or a skipped segment."),
           ("coord", "Field coordinator", "Organises teams, return visits and re-interviews; passes on every PSU replacement."),
           ("dm", "Data management", "Maintains the CAPI, maps and dashboard; produces the alerts; confirms uploads every day."),
           ("qa", "Data quality", "Reviews alerts, decides corrective actions, commissions back-checks and the coverage audit.")],
    foot1="In doubt in the field? Call the supervisor or coordinator before leaving the household: fixing it on the spot is easy, fixing it afterwards is almost impossible.",
    foot2="Sankuru vaccination coverage survey · UNIKIN, Department of Tropical Medicine · November 2026",
)

STEP_COL = [BLUE, BLUE, GREEN, GREEN, GREEN, ORANGE, TEAL, TEAL, PURPLE, PURPLE]
PHASE_OF = [0, 0, 0, 1, 1, 1, 2, 2, 3, 3]

CSS = """
:root{--navy:#12305a;--ink:#1f2933;--muted:#5b6876;--line:#dfe5ec}
*{box-sizing:border-box}
body{margin:0;background:#fff;color:var(--ink);font-family:"Segoe UI",Roboto,Arial,sans-serif}
.poster{width:1400px;margin:0 auto;background:#fff}
.hd{display:grid;grid-template-columns:1.25fr 1fr;background:var(--navy);color:#fff;position:relative;overflow:hidden}
.hd .l{padding:38px 40px 34px}
.hd h1{margin:0;font-size:50px;line-height:1.05;font-weight:800;letter-spacing:-.5px}
.hd h1 span{color:#f5c400;display:block}
.hd .bar{width:110px;height:6px;background:#f5c400;margin:18px 0 16px;border-radius:3px}
.hd p{margin:0;font-size:19px;line-height:1.45;color:#dce8f6;max-width:700px}
.hd .r{position:relative;background:linear-gradient(160deg,#1d4a85,#12305a)}
.hd .r svg{position:absolute;right:0;bottom:0;width:100%;height:100%}
.slogan{position:absolute;right:30px;top:26px;background:#2e8b57;color:#fff;font-size:24px;font-weight:800;padding:12px 20px;transform:rotate(-4deg);border-radius:6px;line-height:1.2;box-shadow:0 4px 0 rgba(0,0,0,.2)}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;padding:22px 26px 6px}
.card{border:2px solid var(--line);border-radius:14px;overflow:hidden;display:flex;flex-direction:column;background:#fff}
.card .top{display:flex;align-items:center;gap:12px;padding:14px 16px 6px}
.num{flex:0 0 52px;height:52px;border-radius:50%;color:#fff;font-size:28px;font-weight:800;display:flex;align-items:center;justify-content:center}
.card h2{margin:0;font-size:23px;line-height:1.15;color:var(--navy)}
.phase{font-size:12px;font-weight:800;letter-spacing:1px;margin-bottom:2px}
.pic{width:100%;height:auto;display:block;background:#f7f9fc;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.card ul{margin:10px 16px 6px 18px;padding:0 0 0 14px;font-size:15.5px;line-height:1.38}
.card li{margin-bottom:6px}
.who{margin:auto 16px 12px;font-size:13.5px;color:var(--muted);border-top:1px dashed var(--line);padding-top:8px}
.who b{color:var(--navy)}
.red{border-color:#e8b4b4;background:#fffafa}
.red h2{color:#c83b3b}
.ri{width:56px;height:50px;flex:0 0 56px}
.rl{display:grid;grid-template-columns:1fr 1fr;gap:8px 10px;padding:8px 14px 14px}
.rl div{display:flex;align-items:center;gap:8px;font-size:14px;line-height:1.25;font-weight:600}
.new{border-color:#f0d27a;background:#fffcf0}
.new ul{font-size:15px}
.new .num{background:#f5c400;color:var(--navy)}
.roles{margin:14px 26px 0;border-radius:14px;background:#eef3f8;padding:16px 20px 18px}
.roles h3{margin:0 0 10px;color:var(--navy);font-size:22px}
.rg{display:grid;grid-template-columns:repeat(5,1fr);gap:14px}
.rg div{background:#fff;border-radius:10px;padding:10px 12px;font-size:14px;line-height:1.35}
.rg svg{width:64px;height:58px;display:block;margin:0 auto 4px}
.rg b{display:block;color:var(--navy);font-size:15.5px;text-align:center;margin-bottom:4px}
.ft{margin:16px 0 0;background:var(--navy);color:#fff;display:grid;grid-template-columns:auto 1fr;gap:20px;align-items:center;padding:18px 30px}
.ft .call{font-size:17px;line-height:1.4}
.ft .phone{width:54px;height:54px}
.ft small{display:block;color:#a9bfdb;font-size:13px;margin-top:6px}
"""


def header_art():
    # village scene with a team, drawn at right of header
    g = '<svg viewBox="0 0 560 300" preserveAspectRatio="xMaxYMax meet">'
    g += DEFS
    g += '<path d="M0 230 Q140 170 280 210 T560 190 L560 300 L0 300 Z" fill="#2c5f3a" opacity=".55"/>'
    g += '<path d="M0 260 Q160 220 320 250 T560 240 L560 300 L0 300 Z" fill="#3f7a4b"/>'
    for x, y, s in [(90, 238, .9), (150, 230, .75), (430, 232, .85), (495, 226, .7)]:
        g += house(x, y, s, fill="#e9d9b8", roof="#7b4a2a", stroke="#5b4630")
    g += ''
    g += person(250, 280, 1.45, tablet=True, cap=True)
    g += person(318, 280, 1.45, vest="#2f6fb0", tablet=True, female=True)
    g += person(380, 280, 1.2, vest="#5a3d7a", shirt="#7f5aa8", female=True)
    g += pin(286, 150, 1.0, "#c83b3b")
    g += '</svg>'
    return g


def build(L):
    cards = []
    for i, (title, bullets, who) in enumerate(L["steps"]):
        col = STEP_COL[i]
        cards.append(
            f'<section class="card" style="border-color:{col}33">'
            f'<div class="top"><div class="num" style="background:{col}">{i+1}</div>'
            f'<div><div class="phase" style="color:{col}">{L["phases"][PHASE_OF[i]]}</div><h2>{title}</h2></div></div>'
            f'{scene(i+1, L)}<ul>' + "".join(f'<li>{b}</li>' for b in bullets) + '</ul>'
            f'<div class="who"><b>{L["who"]} :</b> {who}</div></section>' if L["lang"] == "fr" else
            f'<section class="card" style="border-color:{col}33">'
            f'<div class="top"><div class="num" style="background:{col}">{i+1}</div>'
            f'<div><div class="phase" style="color:{col}">{L["phases"][PHASE_OF[i]]}</div><h2>{title}</h2></div></div>'
            f'{scene(i+1, L)}<ul>' + "".join(f'<li>{b}</li>' for b in bullets) + '</ul>'
            f'<div class="who"><b>{L["who"]}:</b> {who}</div></section>')
    red = (f'<section class="card red"><div class="top"><div class="num" style="background:{RED}">✕</div>'
           f'<div><div class="phase" style="color:{RED}">{L["red_sub"]}</div><h2>{L["red_title"]}</h2></div></div><div class="rl">'
           + "".join(f'<div>{redline_icon(k)}<span>{t}</span></div>' for k, t in enumerate(L["red"])) + '</div></section>')
    new = (f'<section class="card new"><div class="top"><div class="num">!</div>'
           f'<div><div class="phase" style="color:#9a7a00">13 & 16 NOV 2026</div><h2>{L["new_title"]}</h2></div></div><ul>'
           + "".join(f'<li>{t}</li>' for t in L["new"]) + '</ul></section>')
    roles = ('<div class="roles"><h3>' + L["roles_title"] + '</h3><div class="rg">'
             + "".join(f'<div><svg viewBox="-34 -40 68 90">{ROLE_ICON[k]}</svg><b>{n}</b>{d}</div>' for k, n, d in L["roles"]) + '</div></div>')
    phone = (f'<svg class="phone" viewBox="0 0 54 54"><circle cx="27" cy="27" r="27" fill="#f5c400"/>'
             f'<path d="M19 15 q-6 8 0 20 q8 10 18 10 l4 -6 l-8 -6 l-4 3 q-5 -3 -8 -9 l3 -4 l-5 -8 z" fill="{NAVY}"/></svg>')
    html = (f'<!doctype html><html lang="{L["lang"]}"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width, initial-scale=1"><title>{L["title1"]} {L["title2"]}</title>'
            f'<style>{CSS}</style></head><body><div class="poster">'
            f'<header class="hd"><div class="l"><h1>{L["title1"]}<span>{L["title2"]}</span></h1><div class="bar"></div><p>{L["lead"]}</p></div>'
            f'<div class="r">{header_art()}<div class="slogan">{L["slogan"]}</div></div></header>'
            f'<div class="grid">{"".join(cards)}{red}{new}</div>{roles}'
            f'<footer class="ft">{phone}<div class="call"><b>{L["foot1"]}</b><small>{L["foot2"]}</small></div></footer>'
            f'</div></body></html>')
    return html


if __name__ == "__main__":
    out = sys.argv[1]
    for L, name in [(FR, "Process_infographic_FR.html"), (EN, "Process_infographic_EN.html")]:
        open(os.path.join(out, name), "w", encoding="utf-8").write(build(L))
        print("wrote", name)
