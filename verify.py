from pathlib import Path
import re
root = Path(__file__).parent
site = root / 'dist'
expected = {'index.html', 'app.js', 'app.css', 'effects.css'}
assert {p.name for p in site.iterdir()} == expected, 'Only public application files may be deployed'
css = (site / 'effects.css').read_text()
assert not re.search(r'clip-path|gradient|scrollbar|grid(?:-[a-z-]+)?\s*:|display\s*:\s*(?:inline-)?grid|(?:^|[;{])\s*font\s*:|background\s*:[^;}]*url\(', css, re.I)
html = (site / 'index.html').read_text()
assert 'id="workskin"' in html
assert 'src="app.js"' in html and 'href="app.css"' in html
assert not re.search(r'白乌山|何明烁|我在雪山尽头', ''.join(p.read_text() for p in site.iterdir()))
print('PASS: public application only; private manuscript excluded; exported CSS restrictions checked')
