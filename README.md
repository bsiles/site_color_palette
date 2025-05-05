# Site Color Palette Generator

A Python tool that extracts and visualizes color palettes from websites. This tool analyzes a website's CSS and HTML to identify primary, secondary, accent, and neutral colors, then generates a visual representation of the color scheme.

## Features

- Extract color palettes from any website URL
- Identify primary, secondary, accent, and neutral colors
- Generate visual color palette previews
- Save color palette visualizations as images
- Interactive color display with hover effects

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/site_color_palette.git
cd site_color_palette
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Extract colors from a website:
```bash
python main.py extract https://example.com
```

2. Visualize the extracted color palette:
```bash
python main.py visualize
```

## Requirements

- Python 3.7+
- See `requirements.txt` for full list of dependencies

## License

MIT License 