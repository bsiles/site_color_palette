import re
from urllib.parse import urljoin, urlparse

HEX_RE = re.compile(r'#[0-9A-Fa-f]{6}')

NEUTRAL_LUMA_THRESHOLD = 0.08  # tweak to drop greys

def is_hex_colour(token: str) -> bool:
    return bool(HEX_RE.fullmatch(token))

def relative_url(base: str, link: str) -> str:
    """Resolve /styles.css against https://example.com"""
    return link if bool(urlparse(link).netloc) else urljoin(base, link)

def srgb_to_linear(c):  # 0-1 → 0-1
    return c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4

def hex_to_rgb(h: str):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def relative_luminance(hex_code: str) -> float:
    r, g, b = (c / 255 for c in hex_to_rgb(hex_code))
    r, g, b = map(srgb_to_linear, (r, g, b))
    return 0.2126*r + 0.7152*g + 0.0722*b
