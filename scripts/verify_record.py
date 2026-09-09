"""Check every rendered CV record against the master file (requires pdfplumber)."""
from pathlib import Path
import re,unicodedata,json
import pdfplumber
root=Path(__file__).resolve().parents[1]
d=json.loads((root/'app/generated/academic.json').read_text(encoding='utf-8'))
def norm(s):
    s=re.sub(r'\[([^]]+)\]\([^)]+\)',r'\1',str(s))
    return ''.join(c for c in unicodedata.normalize('NFKD',s).casefold() if c.isalnum())
pdf=pdfplumber.open(root/'public/Matthias-Fleckenstein-CV.pdf')
extracted=' '.join(p.extract_text() for p in pdf.pages)
# Font-specific baseline differences can place italic category labels between
# extracted lines even though the page displays them at the paragraph start.
body=norm(re.sub(r'Conferences:|Seminars:','',extracted))
omit={'id','paper_id','portrait','url','website','abstract','biography','sourceHash','type','unit','pdf','appendix','datasets','homepage','course_links','social_links'}
checked=[];missing=[]
def walk(value,path=''):
    if isinstance(value,dict):
        for key,item in value.items():
            if key not in omit:walk(item,path+'.'+key)
    elif isinstance(value,list):
        for i,item in enumerate(value):walk(item,path+f'[{i}]')
    elif len(norm(value))>5:
        checked.append(path)
        if norm(value) not in body:missing.append((path,value))
walk(d)
assert not missing, 'Missing from PDF: '+json.dumps(missing,ensure_ascii=False,indent=2)
assert '<br' not in body and 'abstract' not in body
print(f'Verified {len(checked)} content fields across {len(pdf.pages)} pages; no missing records.')
