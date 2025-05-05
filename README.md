# Site Color Palette Generator

**Purpose:**
This Python tool extracts and visualizes color palettes from any website, making it easy to analyze and hand off color schemes for design or development.

**Main Features
Extract Color Palettes from Websites:**
Given a website URL, the tool fetches the site’s CSS and HTML, analyzes them, and identifies the main colors used.

**Color Classification:**
The script classifies extracted colors into categories:
Primary
Secondary
Accent
Neutral
This helps in understanding the color hierarchy and usage on the site.

**Palette Auto-Optimization:**
The tool can automatically optimize the palette for better hand-off to designers or builders, ensuring the most relevant and visually distinct colors are selected.

**Visualization:**
Generates a visual preview of the color palette, displaying each color group in a clear, organized layout.
Includes interactive features like hover and active states for primary colors.
Can save the visualization as an image for sharing or documentation.

**Headless Functionality:**
The script can run in headless mode, making it suitable for automated workflows or CI/CD pipelines.

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
