from .utils import relative_luminance, hex_to_rgb

def contrast_ratio(fg: str, bg: str) -> float:
    l1, l2 = sorted((relative_luminance(fg), relative_luminance(bg)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)

def is_wcag_aa(fg: str, bg: str, large_text=False) -> bool:
    threshold = 3.0 if large_text else 4.5
    return contrast_ratio(fg, bg) >= threshold
