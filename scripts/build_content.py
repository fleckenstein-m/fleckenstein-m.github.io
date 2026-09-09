"""Generate website data and the complete CV from content/academic.md."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent / 'vendor'))
import json
from content_model import ContentError, load_content
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'content' / 'academic.md'
try:
    data = load_content(SOURCE, ROOT)
except ContentError as error:
    sys.exit(f'Content error: {error}')
(ROOT / 'app' / 'generated').mkdir(parents=True, exist_ok=True)
(ROOT / 'public').mkdir(exist_ok=True)

from build_clean_cv import render_cv
render_cv(data, ROOT)
# Publish new website data only after both validation and CV compilation succeed.
(ROOT / 'app' / 'generated' / 'academic.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')

