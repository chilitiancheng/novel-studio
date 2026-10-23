from pathlib import Path
import re
root = Path(__file__).parent
site = root / 'dist'
expected = {'index.html', 'app.js', 'media.js', 'app.css', 'effects.css'}
public_audio = {'audio/lv_0_20261021200729.mp3'}  # Explicitly requested public music file.
files = {p.relative_to(site).as_posix() for p in site.rglob('*') if p.is_file()}
public_media = files - expected - public_audio
assert expected | public_audio <= files, 'Missing application or existing authorized audio'
for name in public_media:
    assert re.fullmatch(r'media/media-[a-z0-9]+-[a-z0-9]+\.(?:png|jpg|gif|webp|mp4|mp3|m4a|wav|ogg)', name), 'Only user-uploaded media allowed in media directory'
    data = (site / name).read_bytes()
    ext = name.rsplit('.', 1)[1]
    assert 0 < len(data) <= (20 if ext == 'mp4' else 4) * 1024 * 1024, 'Media size limit exceeded'
    signatures = {
        'png': data.startswith(b'\x89PNG'),
        'jpg': data.startswith(b'\xff\xd8\xff'),
        'gif': data[:6] in (b'GIF87a', b'GIF89a'),
        'webp': data[:4] == b'RIFF' and data[8:12] == b'WEBP',
        'mp4': data[4:8] == b'ftyp',
        'm4a': data[4:8] == b'ftyp',
        'mp3': data.startswith(b'ID3') or len(data)>1 and data[0]==255 and data[1]&224==224,
        'wav': data[:4] == b'RIFF' and data[8:12] == b'WAVE',
        'ogg': data[:4] == b'OggS',
    }
    assert signatures[ext], 'Invalid media signature'

for name in public_audio:
    data = (site / name).read_bytes()
    assert len(data) <= 10 * 1024 * 1024 and (data[:3] == b'ID3' or data[0] == 255), 'Invalid audio asset'
css = (site / 'effects.css').read_text()
assert not re.search(r'clip-path|object-fit|gradient|scrollbar|(?:row-|column-)?gap\s*:|grid(?:-[a-z-]+)?\s*:|display\s*:\s*(?:inline-)?grid|(?:^|[;{])\s*font\s*:|background\s*:[^;}]*url\(', css, re.I)
html = (site / 'index.html').read_text()
assert 'id="workskin"' in html
assert re.search(r'src="app\.js(?:\?[^"]*)?"', html) and re.search(r'href="app\.css(?:\?[^"]*)?"', html)
assert not re.search(r'白乌山|何明烁|我在雪山尽头', ''.join((site / name).read_text() for name in expected))
print('PASS: public application only; private manuscript excluded; exported CSS restrictions checked')
