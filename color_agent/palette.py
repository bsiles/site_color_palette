"""
Palette builder  –  pick first non-neutral as primary,
then QA-adjust to pass AA and builder sanity checks.
"""

from __future__ import annotations
from typing import List, Dict
import colorsys
from .color_math import adjust_lightness
from .contrast import contrast_ratio           # you already have this

# ── helpers (unchanged from your post) ───────────────────────
_STEPS = {"50": 1.75, "100": 1.45, "300": 1.15,
          "500": 1.0,  "700": 0.85, "900": 0.55}

def _hex_to_rgb(h): h = h.lstrip("#"); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
def _sat(h): r, g, b = (_/255 for _ in _hex_to_rgb(h)); return colorsys.rgb_to_hls(r, g, b)[2]
def _is_neutral(h, th=.12): return _sat(h) < th
def _distinct(cs, deg=25):
    out, hues = [], []
    for c in cs:
        h = colorsys.rgb_to_hls(*[v/255 for v in _hex_to_rgb(c)])[0] * 360
        if all(abs(h - x) > deg for x in hues): out.append(c); hues.append(h)
    return out
def _rotate(hx, deg):
    r, g, b = (_/255 for _ in _hex_to_rgb(hx))
    h, l, s = colorsys.rgb_to_hls(r, g, b); h = ((h*360 + deg) % 360) / 360
    r2, g2, b2 = colorsys.hls_to_rgb(h, l, s)
    return f"#{int(r2*255):02x}{int(g2*255):02x}{int(b2*255):02x}"
def _scale(base): return {k: adjust_lightness(base, f) for k, f in _STEPS.items()}

# ── AA + tweak helpers ───────────────────────────────────────
AA_NORMAL, AA_LARGE = 4.5, 3.0
def _aa(fg, bg, large=False): return contrast_ratio(fg, bg) >= (AA_LARGE if large else AA_NORMAL)
def _is_dark(hex_code):
    r, g, b = (int(hex_code[i:i+2], 16) for i in (1, 3, 5))
    return (0.2126*r + 0.7152*g + 0.0722*b) < 128
def _tweak_until(hex_code, test, step=0.04, max_iter=12):
    colour = hex_code
    for _ in range(max_iter):
        if test(colour): return colour
        colour = adjust_lightness(colour, 1 - step if _is_dark(colour) else 1 + step)
    return hex_code

# ── main ─────────────────────────────────────────────────────
def build_palette(candidates: List[str]) -> Dict[str, Dict]:
    vivid = [c for c in candidates if not _is_neutral(c)]
    if not vivid:
        vivid = ["#0066ff"]

    base_primary   = vivid[0]
    rest           = _distinct(vivid[1:])
    base_secondary = (rest + [_rotate(base_primary,  30)])[0]
    base_accent    = (rest[1:] + [_rotate(base_primary, -30)])[0]

    palette = {
        "primary":   {**_scale(base_primary),  "foreground": "#FFFFFF"},
        "secondary": {"500": base_secondary,   "foreground": "#FFFFFF"},
        "accent":    {"500": base_accent,      "foreground": "#FFFFFF"},
        "neutral": {
            "0":"#FFFFFF","50":"#F7F9FA","100":"#ECEFF1",
            "300":"#CAD1D6","500":"#8A959E","700":"#4E5B67","900":"#111111"
        },
        "success":{"500":"#12B76A","foreground":"#FFFFFF"},
        "warning":{"500":"#F79009","foreground":"#111111"},
        "error":  {"500":"#D92D20","foreground":"#FFFFFF"},
        "info":   {"500":"#2D8CFF","foreground":"#FFFFFF"},
        "background":"#FFFFFF","surface":"#F7F9FA",
        "text":"#111111","text-muted":"#4E5B67"
    }

    # ── QA PASS ───────────────────────────────────────────────
    # 1. WCAG AA on brand chips vs white
    for role in ("primary", "secondary", "accent"):
        brand = palette[role]["500"]
        palette[role]["500"] = _tweak_until(
            brand,
            lambda c: _aa(c, "#FFFFFF") and _aa("#FFFFFF", c, large=True)
        )

    # 2. Monotonic tone ladder check
    for role in ("primary", "secondary", "neutral"):
        tones = palette[role]
        keys  = [k for k in tones if k.isdigit()]
        for i in range(1, len(keys)):
            prev, cur = keys[i-1], keys[i]
            if (_is_dark(tones[prev]) and not _is_dark(tones[cur])) or \
               (not _is_dark(tones[prev]) and _is_dark(tones[cur])):
                tones[cur] = adjust_lightness(
                    tones[prev],
                    1.12 if _is_dark(tones[prev]) else 0.88
                )

    # 3. Ensure 25° hue gap between brand hues
    def _hue(hex_code):
        r, g, b = (int(hex_code[i:i+2], 16)/255 for i in (1,3,5))
        return colorsys.rgb_to_hls(r, g, b)[0]*360
    hues = []
    for role in ("primary", "secondary", "accent"):
        h = _hue(palette[role]["500"])
        if any(abs(h - h2) < 25 for h2 in hues):
            palette[role]["500"] = _rotate(palette[role]["500"], 30)
        hues.append(_hue(palette[role]["500"]))

    # 4. Neutral/500 legible on white
    if not _aa(palette["neutral"]["500"], "#FFFFFF", large=True):
        palette["neutral"]["500"] = _tweak_until(
            palette["neutral"]["500"],
            lambda c: _aa(c, "#FFFFFF", large=True)
        )

    # 5. Extra builder tokens
    if "300" not in palette["secondary"]:
        palette["secondary"]["300"] = adjust_lightness(palette["secondary"]["500"], 1.15)
    if "600" not in palette["accent"]:
        palette["accent"]["600"] = adjust_lightness(palette["accent"]["500"], 0.85)
        
    def _lighter(hex_code, pct=0.10):
        return adjust_lightness(hex_code, 1 + pct)

    def _darker(hex_code, pct=0.10):
        return adjust_lightness(hex_code, 1 - pct)

    for role in ("primary", "secondary", "accent"):
        base = palette[role]["500"]
        palette[f"{role}Hover"]   = _lighter(base, 0.12)   # +12 % lightness
        palette[f"{role}Active"]  = _darker(base, 0.12)    # –12 % lightness

    # Hero gradient: very light tint → base tone
    palette["heroGradientStart"] = _lighter(palette["primary"]["100"]
                                            if "100" in palette["primary"]
                                            else palette["primary"]["50"], 0.10)
    palette["heroGradientEnd"]   = palette["primary"]["500"]
    
    return palette