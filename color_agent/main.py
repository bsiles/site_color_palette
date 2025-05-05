#!/usr/bin/env python3
"""
color_agent.main
– CLI entry-point for the headless colour-extraction agent.
"""

import argparse, json, pathlib, sys, logging

# local package imports (all dotted → within color_agent)
from .css_extractor   import extract as css_extract
from .image_extractor import download_image, dominant_colours, simple_mode
from .palette         import build_palette
from .visualize       import show_palette     # needs matplotlib installed

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("color-agent")

# ──────────────────────────────────────────────────────────────
# CLI ARGUMENTS
# ──────────────────────────────────────────────────────────────
def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Extract a full design-system palette from a website or logo."
    )
    p.add_argument("--url", required=True,
                   help="URL of the site whose colours to analyse")
    p.add_argument("--out", default="-",
                   help="Write palette JSON to FILE or '-' (stdout, default)")
    p.add_argument("--preview", action="store_true",
                   help="Show a swatch window of the palette")
    p.add_argument("--save-preview",
                   help="Path to save the preview PNG/SVG (optional)")
    # future-proof: logo mode (disabled unless you wire it up)
    # p.add_argument("--logo", help="Path or URL of logo image")

    return p.parse_args()

# ──────────────────────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────────────────────
def from_css(url: str):
    log.info(f"‣ scraping CSS from {url}")
    colours = css_extract(url)
    log.info(f"  found {len(colours)} tokens → {colours[:10]}")
    return build_palette(colours)

def from_logo(path: str):
    log.info(f"‣ extracting palette from {path}")
    img = download_image(path)
    try:
        colours = dominant_colours(img)
    except ImportError:
        colours = [simple_mode(img)]
    log.info(f"  top colours → {colours}")
    return build_palette(colours)

# ──────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────
def main() -> int:
    try:
        args = parse_args()

        log.info(f"Analyzing colours from: {args.url}")
        palette = from_css(args.url)          # switch to from_logo() if needed

        # JSON output
        out_json = json.dumps(palette, indent=2)
        if args.out == "-":
            print(out_json)
        else:
            pathlib.Path(args.out).write_text(out_json)
            log.info(f"✓ palette JSON written → {args.out}")

        # Visual preview (window or file)
        if args.preview or args.save_preview:
            show_palette(
                palette,
                title=f"Palette preview for {args.url}",
                save_path=args.save_preview
            )

        return 0
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())