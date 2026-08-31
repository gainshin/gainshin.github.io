import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

# Let's inspect the entire structure and create the updated HTML
html_path = Path("assets/course/teaching_brief_market_map.html")
orig_text = html_path.read_text(encoding="utf-8")

print("Original text size:", len(orig_text))
