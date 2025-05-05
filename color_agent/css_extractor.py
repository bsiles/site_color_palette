"""
CSS colour extractor  –  frequency-ordered
Grabs colours from:
  • external <link rel="stylesheet"...>
  • <style> blocks
  • inline style="…"
Returns them sorted by descending frequency (most_common → least).
"""

from __future__ import annotations
import re, requests, colorsys
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import Counter

HEX_RE = re.compile(r'#(?:[0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})\b')
RGB_RE = re.compile(r'rgb\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*\)')
HSL_RE = re.compile(r'hsl[a]?\(\s*(\d{1,3})\s*,\s*(\d{1,3})%\s*,\s*(\d{1,3})%\s*\)')

def _norm(hx:str)->str: return "#"+"".join(c*2 for c in hx[1:]) if len(hx)==4 else hx.lower()
def _rgb_hex(r,g,b): return f"#{int(r):02x}{int(g):02x}{int(b):02x}"
def _hsl_hex(h,s,l):
    h,s,l = map(float,(h,s,l)); import colorsys
    r,g,b = colorsys.hls_to_rgb(h/360,l/100,s/100)
    return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"

def _collect(css:str)->list[str]:
    out=[_norm(c) for c in HEX_RE.findall(css)]
    out+=[_rgb_hex(r,g,b) for r,g,b in RGB_RE.findall(css)]
    out+=[_hsl_hex(h,s,l) for h,s,l in HSL_RE.findall(css)]
    return out

def _abs(base,link): return link if urlparse(link).netloc else urljoin(base,link)

def extract(page_url:str, top_k:int=20)->list[str]:
    try: html=requests.get(page_url,timeout=10).text
    except Exception: return []

    soup=BeautifulSoup(html,"html.parser")
    bucket:Counter=Counter()

    def _see(css:str): bucket.update(_collect(css))

    for l in soup.find_all("link",rel=lambda v:v and "stylesheet" in v.lower()):
        href=l.get("href"); 
        if not href: continue
        try: _see(requests.get(_abs(page_url,href),timeout=10).text)
        except Exception: pass

    for tag in soup.find_all("style"):
        _see(tag.get_text())

    for tag in soup.find_all(style=True):
        _see(tag["style"])

    return [c.lower() for c,_ in bucket.most_common(top_k)]
