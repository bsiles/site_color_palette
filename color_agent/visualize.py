"""
color_agent.visualize
---------------------------------
Preview primary, secondary, accent, and neutral rows – each full height.
"""

from typing import Dict, Any, List
import matplotlib.pyplot as plt
import colorsys

# rows to draw, in order
_ROWS: List[str] = ["primary", "secondary", "accent", "neutral"]


def _ordered_keys(block: Dict[str, Any]) -> List[str]:
    numeric = [k for k in block if k.isdigit()]
    return sorted(numeric, key=lambda k: int(k)) or ["500"]


def _is_dark(hex_code: str) -> bool:
    r, g, b = (int(hex_code[i : i + 2], 16) / 255 for i in (1, 3, 5))
    _, l, _ = colorsys.rgb_to_hls(r, g, b)
    return l < 0.35


def show_palette(
    palette: Dict[str, Any],
    title: str = "",
    save_path: str | None = None,
) -> None:
    """Draw the palette rows; show or save image."""
    rows = [r for r in _ROWS if r in palette]
    
    # Create a figure with fixed height per row
    row_height = 1.0
    total_height = len(rows) * row_height
    fig, axes = plt.subplots(len(rows), 1, figsize=(10, total_height))
    
    # If only one row, make axes a list
    if len(rows) == 1:
        axes = [axes]
    
    # Set up each row
    for ax, role in zip(axes, rows):
        ax.axis("off")
        ax.set_facecolor("#d9d9d9")
        
        swatch = palette[role]
        keys = _ordered_keys(swatch)
        box_w = 1 / len(keys)
        
        # Draw each color in the row
        for i, k in enumerate(keys):
            clr = swatch[k]
            ax.add_patch(plt.Rectangle(
                (i * box_w, 0), box_w, 1,
                facecolor=clr, edgecolor="#555", linewidth=0.6)
            )
            ax.text(i * box_w + box_w / 2, 0.5, k,
                    ha="center", va="center", fontsize=8,
                    color="#fff" if _is_dark(clr) else "#000")
        
        # Add role label
        ax.text(-0.05, 0.5, role,
                ha="right", va="center",
                fontsize=10, fontweight="bold")
    
    if title:
        fig.suptitle(title, fontsize=12, y=0.95)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=180, bbox_inches='tight')
        print(f"✓ saved preview → {save_path}")
    else:
        plt.show()
