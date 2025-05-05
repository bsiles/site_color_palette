# color_agent/color_math.py
"""
Color manipulation utilities for the Color Agent.
"""

import colorsys
from typing import Tuple

def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    """Convert RGB tuple to hex color."""
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def adjust_lightness(hex_color: str, factor: float) -> str:
    """
    Adjust the lightness of a color by a factor.
    factor > 1 makes the color lighter
    factor < 1 makes the color darker
    """
    # Convert hex to RGB
    r, g, b = hex_to_rgb(hex_color)
    
    # Convert RGB to HSL
    h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
    
    # Adjust lightness
    new_l = min(1.0, max(0.0, l * factor))
    
    # Convert back to RGB
    r, g, b = colorsys.hls_to_rgb(h, new_l, s)
    
    # Convert to hex
    return rgb_to_hex((int(r * 255), int(g * 255), int(b * 255)))
