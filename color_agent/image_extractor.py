from collections import Counter
from io import BytesIO
from PIL import Image, ImageStat
import requests, numpy as np

def download_image(url_or_path: str) -> Image.Image:
    if url_or_path.startswith("http"):
        resp = requests.get(url_or_path, timeout=10)
        resp.raise_for_status()
        return Image.open(BytesIO(resp.content)).convert("RGB")
    return Image.open(url_or_path).convert("RGB")

def dominant_colours(img: Image.Image, k: int = 5) -> list[str]:
    # resize for speed
    img = img.copy().resize((80, 80))
    pixels = np.array(img).reshape(-1, 3)

    # K-means in RGB
    from sklearn.cluster import KMeans  # optional heavy dep
    km = KMeans(n_clusters=k, n_init="auto").fit(pixels)
    centers = km.cluster_centers_.astype(int)

    def to_hex(rgb): return "#" + "".join(f"{c:02x}" for c in rgb)
    return [to_hex(c) for c in centers]

def simple_mode(img: Image.Image) -> str:
    """fallback – most common pixel"""
    img = img.copy().resize((50, 50))
    pixels = list(img.getdata())
    rgb, _ = Counter(pixels).most_common(1)[0]
    return "#" + "".join(f"{c:02x}" for c in rgb)
