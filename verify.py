from pathlib import Path
import re
root = Path(__file__).parent
site = root / 'dist'
expected = {'index.html', 'app.js', 'app.css', 'effects.css'}
public_audio = {'audio/lv_0_20261021200729.mp3'}  # Explicitly requested public music file.
files = {p.relative_to(site).as_posix() for p in site.rglob('*') if p.is_file()}
assert files == expected | public_audio, 'Only public application and explicitly authorized music may be deployed'
for name in public_audio:
    data = (site / name).read_bytes()
    assert len(data) <= 10 * 1024 * 1024 and (data[:3] == b'ID3' or data[0] == 255), 'Invalid audio asset'
css = (site / 'effects.css').read_text()
assert not re.search(r'clip-path|object-fit|gradient|scrollbar|(?:row-|column-)?gap\s*:|grid(?:-[a-z-]+)?\s*:|display\s*:\s*(?:inline-)?grid|(?:^|[;{])\s*font\s*:|background\s*:[^;}]*url\(', css, re.I)
html = (site / 'index.html').read_text()
assert 'id="workskin"' in html
assert 'src="app.js"' in html and 'href="app.css"' in html
assert not re.search(r'白乌山|何明烁|我在雪山尽头', ''.join((site / name).read_text() for name in expected))
print('PASS: public application only; private manuscript excluded; exported CSS restrictions checked')
