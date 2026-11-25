from pathlib import Path
from zipfile import ZipFile
from lxml import etree
from pypdf import PdfReader
import json,hashlib
p=Path(__file__).resolve().parent
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','m':'http://schemas.openxmlformats.org/officeDocument/2006/math'}
result={}
for name,path in [('source',p.parent/'draft-review-source.docx'),('revised',p/'Skripsi_Zia_Ulhaq_Revisi.docx')]:
 with ZipFile(path) as z:
  xml=etree.fromstring(z.read('word/document.xml'))
  result[name]={'equations':len(xml.xpath('//m:oMath',namespaces=ns)),'tables':len(xml.xpath('//w:tbl',namespaces=ns)),'media':sorted(hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.startswith('word/media/'))}
assert result['source']['equations']==result['revised']['equations']
assert result['source']['media']==result['revised']['media']
pages=[x.extract_text() or '' for x in PdfReader(p/'Skripsi_Zia_Ulhaq_Revisi.pdf').pages]
text='\n'.join(pages)
for bad in ['Error!','Standarr','Kabupaten Bandung','DJIKSTRA']:
 assert bad not in text,bad
assert len(pages)==126
print('PASS: equations and original media preserved; 126 pages; no checked field errors or stale names.')
print('TOC back matter:',[x for x in text.splitlines() if 'DAFTAR PUSTAKA' in x or 'LAMPIRAN ' in x][:4])
(p/'final-check.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
