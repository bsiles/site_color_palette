"""
Palette builder  –  primary = first non-neutral in frequency list
Secondary + accent = next two distinct hues, or hue-rotations if missing.
Neutral ramp & semantic colours unchanged.
"""

from __future__ import annotations
from typing import List, Dict
import colorsys
from .color_math import adjust_lightness

_STEPS={"50":1.75,"100":1.45,"300":1.15,"500":1.0,"700":0.85,"900":0.55}

def _hex_to_rgb(h): h=h.lstrip("#"); return tuple(int(h[i:i+2],16) for i in (0,2,4))
def _sat(h): r,g,b=(_/255 for _ in _hex_to_rgb(h)); return colorsys.rgb_to_hls(r,g,b)[2]
def _is_neutral(h,th=.12): return _sat(h)<th
def _distinct(cs,deg=25):
    out,hues=[],[]
    for c in cs:
        h=colorsys.rgb_to_hls(*[v/255 for v in _hex_to_rgb(c)])[0]*360
        if all(abs(h-x)>deg for x in hues): out.append(c); hues.append(h)
    return out
def _rotate(hx,deg):
    r,g,b=(_/255 for _ in _hex_to_rgb(hx))
    h,l,s=colorsys.rgb_to_hls(r,g,b); h=((h*360+deg)%360)/360
    r2,g2,b2=colorsys.hls_to_rgb(h,l,s)
    return f"#{int(r2*255):02x}{int(g2*255):02x}{int(b2*255):02x}"
def _scale(base): return {k:adjust_lightness(base,f) for k,f in _STEPS.items()}

def build_palette(candidates:List[str])->Dict[str,Dict]:
    vivid=[c for c in candidates if not _is_neutral(c)]
    if not vivid: vivid=["#0066ff"]

    base_primary=vivid[0]
    rest=_distinct(vivid[1:])
    base_secondary=(rest+[_rotate(base_primary,30)])[0]
    base_accent   =(rest[1:]+[_rotate(base_primary,-30)])[0]

    return {
        "primary":   {**_scale(base_primary),"foreground":"#FFFFFF"},
        "secondary": {"500":base_secondary,"foreground":"#FFFFFF"},
        "accent":    {"500":base_accent,"foreground":"#FFFFFF"},
        "neutral": {
            "0":"#FFFFFF","50":"#F7F9FA","100":"#ECEFF1",
            "300":"#CAD1D6","500":"#8A959E","700":"#4E5B67","900":"#111111"},
        "success":{"500":"#12B76A","foreground":"#FFFFFF"},
        "warning":{"500":"#F79009","foreground":"#111111"},
        "error":  {"500":"#D92D20","foreground":"#FFFFFF"},
        "info":   {"500":"#2D8CFF","foreground":"#FFFFFF"},
        "background":"#FFFFFF","surface":"#F7F9FA",
        "text":"#111111","text-muted":"#4E5B67"
    }
