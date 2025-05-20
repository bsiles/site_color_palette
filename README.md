# Site Color Palette Generator

## Overview

Site Color Palette Generator is a Python tool that extracts and visualizes
color palettes from websites. It analyzes a site's CSS and HTML to
identify primary, secondary, accent, and neutral colors, then generates
a visual representation of the color scheme. This is useful for designers
and developers looking to quickly understand or replicate a website's
visual identity.

## Tech Stack

*   Python 3.7+
*   Pillow (image processing)
*   requests (HTTP requests)
*   Beautiful Soup 4 (HTML/CSS parsing)
*   colorthief (dominant color extraction)
*   webcolors (color name mapping)
*   NumPy (numerical operations)
*   scikit-learn (color clustering)
*   Matplotlib (palette visualization)

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/bsiles/site_color_palette.git
cd site_color_palette

# 2. Create and activate a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the development server (extract palette from a URL)
python color_agent/main.py --url https://example.com --preview

# 5. Run tests (No dedicated test suite found)
# (Manual testing by running extraction and visualization)
```

## Environment Variables

No environment variables are required for this project.

## Available Commands

| Command                                                                 | Description                                                                 | Use Case     |
| :---------------------------------------------------------------------- | :-------------------------------------------------------------------------- | :----------- |
| `pip install -r requirements.txt`                                       | Installs necessary Python packages.                                         | Setup        |
| `python color_agent/main.py --url <URL>`                                | Extracts palette from `<URL>` and prints JSON to console.                   | Dev / Prod   |
| `python color_agent/main.py --url <URL> --out <FILE.json>`              | Extracts palette from `<URL>` and saves it to `<FILE.json>`.                | Dev / Prod   |
| `python color_agent/main.py --url <URL> --preview`                      | Extracts palette from `<URL>` and displays an interactive preview window.   | Dev          |
| `python color_agent/main.py --url <URL> --save-preview <PATH.png/svg>`  | Extracts palette from `<URL>` and saves the preview image to `<PATH>`.        | Dev / Prod   |

## Project Structure

```
.
├── .git/               # Git version control files
├── .venv/              # Python virtual environment (if created)
├── color_agent/        # Main application code
│   ├── __init__.py
│   ├── color_math.py   # Color manipulation and conversion
│   ├── contrast.py     # Contrast calculation utilities
│   ├── css_extractor.py # Extracts colors from CSS
│   ├── image_extractor.py# Extracts colors from images (logo mode)
│   ├── main.py         # CLI entry point
│   ├── palette.py      # Palette generation and classification
│   ├── utils.py        # Helper functions
│   └── visualize.py    # Generates palette visualization
├── .gitignore          # Specifies intentionally untracked files
├── README.md           # This file
├── requirements.txt    # Project dependencies
├── palette.json        # Example output (if generated)
└── palette.png         # Example visualization (if generated)
```
*   `color_agent/`: Contains all the core logic for color extraction,
    processing, and visualization.
*   Output files (`palette.json`, `*.png`) are typically generated in the
    root directory or a user-specified location.

## Testing

Currently, there is no automated test suite (e.g., unit or integration
tests). Testing is performed manually by running the extraction and
visualization commands with various website URLs.

To lint the code, you can use a tool like `pylint` or `flake8`:
```bash
pip install pylint
pylint color_agent/
```

## Deployment

This project is primarily a command-line tool and does not have specific
deployment scripts for Docker, Vercel, or other cloud platforms. It can be
run in any environment where Python and its dependencies are installed.
The headless nature of `main.py` allows it to be integrated into
automated workflows.
