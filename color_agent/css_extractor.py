import re, requests
from collections import Counter
from bs4 import BeautifulSoup
from pathlib import Path
from .utils import HEX_RE, relative_url

def download_css(url: str) -> str:
    return requests.get(url, timeout=10).text

def colours_from_stylesheet(url: str) -> list[str]:
    css = download_css(url)
    return HEX_RE.findall(css)

def url_to_css_links(page_url: str) -> list[str]:
    html = requests.get(page_url, timeout=10).text
    soup = BeautifulSoup(html, "html.parser")
    links = [
        relative_url(page_url, l["href"])
        for l in soup.find_all("link", rel=lambda v: v and "stylesheet" in v.lower())
        if l.get("href")
    ]
    return links

def extract(page_url: str, top_k: int = 12) -> list[str]:
    """Extract common colors from CSS files linked in the page."""
    print(f"‣ scraping CSS from {page_url}")
    
    # Get the page content
    response = requests.get(page_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find all CSS links
    css_urls = []
    for link in soup.find_all("link", rel="stylesheet"):
        href = link.get("href", "")
        if href:
            # Handle relative URLs
            if href.startswith("//"):
                href = "https:" + href
            elif href.startswith("/"):
                # Get the base URL
                from urllib.parse import urlparse
                parsed = urlparse(page_url)
                base_url = f"{parsed.scheme}://{parsed.netloc}"
                href = base_url + href
            css_urls.append(href)
    
    # Extract colors from each CSS file
    all_colors = []
    for css_url in css_urls:
        try:
            css_response = requests.get(css_url)
            css_response.raise_for_status()
            css_content = css_response.text
            
            # Extract hex colors
            hex_colors = re.findall(r"#[0-9a-fA-F]{6}", css_content)
            all_colors.extend(hex_colors)
        except Exception as e:
            print(f"Error: {str(e)}")
            continue
    
    # Count color frequencies
    color_counts = Counter(all_colors)
    
    # Return top k most common colors
    return [color for color, _ in color_counts.most_common(top_k)]
