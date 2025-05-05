# color_agent/palette.py  –  full design-system palette generator
from typing import List
from .color_math import adjust_lightness      # ← relative import – keep the dot

_NEUTRAL_SCALE = {
    "0":  "#FFFFFF", "50":  "#F7F9FA", "100": "#ECEFF1",
    "300": "#CAD1D6", "500": "#8A959E", "700": "#4E5B67", "900": "#111111",
}

_SEMANTICS = {
    "success":  {"500": "#12B76A", "foreground": "#FFFFFF"},
    "warning":  {"500": "#F79009", "foreground": "#111111"},
    "error":    {"500": "#D92D20", "foreground": "#FFFFFF"},
    "info":     {"500": "#2D8CFF", "foreground": "#FFFFFF"},
}

_STEPS = {      # multiplicative factors relative to the 500 tone
    "50":  1.75,
    "100": 1.45,
    "300": 1.15,
    "500": 1.00,   # base
    "700": 0.85,
    "900": 0.55,
}

def _build_scale(base_hex: str) -> dict:
    """Generate 50-900 tones around base_hex."""
    return {k: adjust_lightness(base_hex, f) for k, f in _STEPS.items()}

def build_palette(candidates: List[str]) -> dict:
    """
    Turn colour candidates → full design-system palette.

    candidates[0] = primary, [1] = secondary, [2] = accent.
    Fallbacks kick in if list is short.
    """
    base_primary   = (candidates + ["#1A6CAB"])[0]
    base_secondary = (candidates + ["#FF7A00", "#1A6CAB"])[1]
    base_accent    = (candidates + ["#36C6F0"])[2]

    return {
        "primary":   {**_build_scale(base_primary),   "foreground": "#FFFFFF"},
        "secondary": {**_build_scale(base_secondary), "foreground": "#FFFFFF"},
        "accent":    {"500": base_accent, "foreground": "#FFFFFF"},
        "neutral":   _NEUTRAL_SCALE,
        **_SEMANTICS,
        "background": _NEUTRAL_SCALE["0"],
        "surface":    _NEUTRAL_SCALE["50"],
        "text":       _NEUTRAL_SCALE["900"],
        "text-muted": _NEUTRAL_SCALE["700"],
    }
